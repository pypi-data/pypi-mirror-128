import torch
import torch.nn as nn
import torch.nn.functional as F

class WaveGlowLoss(nn.Module):
    def __init__(self, sigma=1.0):
        super(WaveGlowLoss, self).__init__()
        
        self.sigma = sigma
        
    def forward(self, outputs):
        z, log_det_W_list, log_s_list = outputs
        
        log_W_total = 0
        log_s_total = 0
        for i in range(len(log_det_W_list)):
            log_W_total += torch.sum(log_det_W_list[i])
            log_s_total += torch.sum(log_s_list[i])
        
        loss = torch.sum(z*z)/(2*self.sigma*self.sigma) - log_W_total - log_s_total
        loss = loss/(z.size(0)*z.size(1)*z.size(2))
        
        return loss

class Invertible1x1Conv(nn.Module):
    def __init__(self, channel):
        super(Invertible1x1Conv, self).__init__()

        self.conv = nn.Conv1d(channel, channel, kernel_size=1, stride=1, padding=0, bias=False)

        W = torch.linalg.qr(torch.FloatTensor(channel, channel).normal_())[0]

        if torch.det(W) < 0:
            W[:, 0] = -1*W[:, 0]

        W = W.view(channel, channel, 1)

        self.conv.weight.data = W

    def forward(self, audio):
        batch_size, length = audio.size(0), audio.size(2)

        W = self.conv.weight.squeeze()

        audio = self.conv(audio)

        log_det_W = batch_size*length*torch.logdet(W)

        return audio, log_det_W

    def invert(self, z):

        W = self.conv.weight.squeeze().detach()
        W_invert = W.inverse().unsqueeze(-1)

        audio = F.conv1d(z, W_invert, bias=None, stride=1, padding=0)

        return audio

@torch.jit.script
def fused_add_tanh_sigmoid_multiply(input_a, input_b, n_channels):
    n_channels_int = n_channels[0]
    in_act = input_a + input_b
    t_act = torch.tanh(in_act[:,:n_channels_int])
    s_act = torch.sigmoid(in_act[:,n_channels_int:])
    acts = t_act*s_act
    
    return acts

class WaveNet(nn.Module):
    def __init__(self, n_audio_channels, n_mel_channels, n_layers, n_channels, kernel_size):
        super(WaveNet, self).__init__()
        
        self.n_layers = n_layers
        self.n_channels = n_channels
        
        start = nn.Conv1d(n_audio_channels, n_channels, 1)
        self.start = nn.utils.weight_norm(start, name='weight')
        
        self.end = nn.Conv1d(n_channels, 2*n_audio_channels, 1) # 2*n_audio_channels for log_s and t
        self.end.weight.data.zero_()
        self.end.bias.data.zero_()
        
        cond_layer = nn.Conv1d(n_mel_channels, 2*n_channels*n_layers, 1)
        self.cond_layer = nn.utils.weight_norm(cond_layer, name='weight')
        
        self.in_layers = nn.ModuleList()
        self.res_skip_layers = nn.ModuleList()
        
        for i in range(n_layers):
            dilation = 2**i
            padding = (kernel_size*dilation - dilation)//2
            in_layer = nn.Conv1d(n_channels, 2*n_channels, kernel_size, dilation=dilation, padding=padding)
            in_layer = nn.utils.weight_norm(in_layer, name='weight')
            self.in_layers.append(in_layer)
            
            if i < n_layers - 1:
                res_skip_channels = 2*n_channels
            else:
                res_skip_channels = n_channels
            res_skip_layer = nn.Conv1d(n_channels, res_skip_channels, 1)
            res_skip_layer = nn.utils.weight_norm(res_skip_layer, name='weight')
            self.res_skip_layers.append(res_skip_layer)
            
            
    def forward(self, x):
        spect, audio = x
        
        n_channels_tensor = torch.IntTensor([self.n_channels])
        
        audio = self.start(audio)
        output = torch.zeros_like(audio)
        
        spect = self.cond_layer(spect)
        
        for i in range(self.n_layers):
            spect_offset = i*2*self.n_channels
            y = self.in_layers[i](audio) 
            spect_y = spect[:,spect_offset:spect_offset+2*self.n_channels]
            acts = fused_add_tanh_sigmoid_multiply(y, spect_y, n_channels_tensor)
            
            res_skip_acts = self.res_skip_layers[i](acts)
            
            if i < self.n_layers - 1:
                audio = audio + res_skip_acts[:,:self.n_channels]
                output = output + res_skip_acts[:,self.n_channels:]
            else:
                output = output + res_skip_acts
        
        output = self.end(output)
        
        return output

class AffineCoupling(nn.Module):
    def __init__(self, n_audio_channels, n_mel_channels, WaveNet_config):
        super(AffineCoupling, self).__init__()
        
        self.WN = WaveNet(n_audio_channels, n_mel_channels, **WaveNet_config)
    
    def forward(self, x):
        spect, audio = x
        
        n_half = audio.size(1)//2
        
        audio_0 = audio[:,:n_half]
        audio_1 = audio[:,n_half:]
        
        output = self.WN((spect, audio_0))
        
        log_s = output[:,n_half:]
        t = output[:,:n_half]
        
        audio_1 = torch.exp(log_s)*audio_1 + t
        
        audio = torch.cat((audio_0, audio_1), 1)
        
        return audio, log_s
        
    def invert(self, y):
        spect, z = y
        n_half = z.size(1)//2
        
        z_0 = z[:,:n_half]
        z_1 = z[:,n_half:]
        
        with torch.no_grad():
            output = self.WN((spect, z_0))
        
        log_s = output[:,n_half:]
        t = output[:,:n_half]
        
        audio_1 = (z_1 - t)/torch.exp(log_s)  
        audio_0 = z_0
        
        audio = torch.cat((audio_0, audio_1), 1)
        
        return audio

class Flow(nn.Module):
    def __init__(self, n_audio_channels, n_WN_channels, n_mel_channels, WaveNet_config):
        super(Flow, self).__init__()
        
        self.convinv = Invertible1x1Conv(n_audio_channels)
        self.affine_coupling = AffineCoupling(n_WN_channels, n_mel_channels, WaveNet_config)
    
    def forward(self, x):
        spect, audio = x
        
        audio, log_det_W = self.convinv(audio)
        
        audio, log_s = self.affine_coupling((spect, audio))
        
        return audio, log_det_W, log_s
    
    def invert(self, y):
        
        audio = self.affine_coupling.invert(y)      
        audio = self.convinv.invert(audio)
        
        return audio    
