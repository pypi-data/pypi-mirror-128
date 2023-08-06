import torch
from vietvocoder.stft import STFT

class Denoiser(torch.nn.Module):
    """ Removes model bias from audio produced with waveglow """

    def __init__(self, waveglow, filter_length=1024, hop_length=256,
                 win_length=1024, mode='normal'):
        super(Denoiser, self).__init__()
        
        dtype = waveglow.upsampling_spect.weight.dtype
        self.device = waveglow.upsampling_spect.weight.device
        
        self.stft = STFT(filter_length=filter_length, hop_length=hop_length, win_length=win_length)
        
        self.stft = self.stft.to(self.device)

        if mode == 'zeros':
            mel_input = torch.zeros(
                (1, 80, 88),
                dtype=dtype,
                device=self.device)
        elif mode == 'normal':
            mel_input = torch.randn(
                (1, 80, 88),
                dtype=dtype,
                device=self.device)
        else:
            raise Exception("Mode {} if not supported".format(mode))
        
        
        with torch.no_grad():
            bias_audio = waveglow.infer(mel_input, sigma=0.0).float()
            bias_spec, _ = self.stft.transform(bias_audio)
        
        self.register_buffer('bias_spec', bias_spec[:, :, 0][:, :, None])

    def forward(self, audio, strength=0.01):
        audio = audio.to(self.device).float()
        audio_spec, audio_angles = self.stft.transform(audio)
        audio_spec_denoised = audio_spec - self.bias_spec * strength
        audio_spec_denoised = torch.clamp(audio_spec_denoised, 0.0)
        audio_denoised = self.stft.inverse(audio_spec_denoised, audio_angles)
        return audio_denoised

