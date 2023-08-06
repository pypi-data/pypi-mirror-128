import torch
import torch.nn as nn
from vietvocoder.model.layers import Flow

class WaveGlow(nn.Module):
    def __init__(self, n_mel_channels, n_flows, n_group, n_early_every, n_early_size, WaveNet_config):
        super(WaveGlow, self).__init__()
        
        assert(n_group % 2 == 0)
        
        self.n_mel_channels = n_mel_channels
        self.n_flows = n_flows
        self.n_group = n_group
        self.n_early_every = n_early_every
        self.n_early_size = n_early_size
        self.WaveNet_config = WaveNet_config
        
        self.upsampling_spect = nn.ConvTranspose1d(n_mel_channels, n_mel_channels, 1024,
                                                  stride=256 #hop_length
                                                  )
        
        self.flows = nn.ModuleList()
        
        n_WN_channels = n_group//2
        n_audio_channels = n_group
        
        for i in range(self.n_flows):
            if i % self.n_early_every == 0 and i > 0:
                n_WN_channels = n_WN_channels - self.n_early_size//2
                n_audio_channels = n_audio_channels - self.n_early_size
                
            flow = Flow(n_audio_channels, n_WN_channels, n_mel_channels*n_group, WaveNet_config)
            self.flows.append(flow)
            
        self.n_audio_channels = n_audio_channels
        
    def forward(self, x):
        spect, audio = x
        
        spect = self.upsampling_spect(spect)
        assert(spect.size(2) >= audio.size(1))
        if spect.size(2) > audio.size(1):
            spect = spect[:,:,:audio.size(1)]
        
        spect = spect.unfold(2, self.n_group, self.n_group).permute(0, 2, 1, 3)
        spect = spect.flatten(-2).permute(0, 2, 1)
        
        audio = audio.unfold(1, self.n_group, self.n_group) # squeeze operation Bx2000x8
        audio = audio.permute(0, 2, 1)
       
        log_det_W_list = []
        log_s_list = []
        output = []
        
        for i in range(self.n_flows):
            if i % self.n_early_every == 0 and i > 0:
                early_output = audio[:, :self.n_early_size]
                audio = audio[:,self.n_early_size:]
                
                output.append(early_output)
            
            audio, log_det_W, log_s = self.flows[i]((spect, audio))
            
            log_det_W_list.append(log_det_W)
            log_s_list.append(log_s)
        
        output.append(audio)
        
        z = torch.cat(output, 1)
        
        return z, log_det_W_list, log_s_list
    
    def infer(self, spect, sigma=1.0):
        device = spect.device
        
        with torch.no_grad():
            spect = self.upsampling_spect(spect)
        
        time_cutoff = self.upsampling_spect.kernel_size[0] - self.upsampling_spect.stride[0]
        spect = spect[:, :, :-time_cutoff]
        
        spect = spect.unfold(2, self.n_group, self.n_group).permute(0, 2, 1, 3)
        spect = spect.flatten(-2).permute(0, 2, 1)
        
        z = torch.FloatTensor(spect.size(0), self.n_audio_channels, spect.size(2)).normal_()
        z = z.to(device)
        z = z*sigma
        
        for i in reversed(range(self.n_flows)):
            z = self.flows[i].invert((spect, z))
            
            if i % self.n_early_every == 0 and i > 0:
                z_early = torch.FloatTensor(spect.size(0), self.n_early_size, spect.size(2)).normal_()
                z_early = z_early.to(device)
                z = torch.cat((z_early*sigma, z), 1)
        
        audio = z.permute(0, 2, 1).flatten(-2)
        
        return audio
