import torch
from vietvocoder.model.waveglow import WaveGlow
from vietvocoder.model.denoiser import Denoiser

class Predictor():
    def __init__(self, config, weight, device):
        
        data_config = config['data_config']
        waveglow_config = config['waveglow_config']
        self.device = device

        self.model = WaveGlow(**waveglow_config)
        self.model.eval()
        self.model.load_state_dict(torch.load(weight))

        if self.device.startswith('cuda'):
            self.model = self.model.to(self.device)

        self.denoiser = Denoiser(self.model, 
                data_config['filter_length'],
                data_config['hop_length'],
                data_config['win_length']
                )

        

    def predict(self, mel, sigma=1.0, denoise_strength=0.01):
        mel = torch.from_numpy(mel)
        mel = mel[None,:]
        mel = mel.to(self.device)
        
        with torch.no_grad():
            sample_audios = self.model.infer(mel, sigma=sigma)
        
        denoise_audios = self.denoiser(sample_audios, denoise_strength)
        denoise_audios = denoise_audios[0].cpu().numpy()

        return denoise_audios
