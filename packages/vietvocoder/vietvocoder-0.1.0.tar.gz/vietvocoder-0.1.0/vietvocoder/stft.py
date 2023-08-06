import torch
import torch.nn as nn

from scipy.signal import get_window
from librosa.util import pad_center, tiny
from librosa.filters import mel as librosa_mel_fn

def dynamic_range_compression(x, C=1, clip_val=1e-5):
    """
    PARAMS
    ------
    C: compression factor
    """
    return torch.log(torch.clamp(x, min=clip_val) * C)


def dynamic_range_decompression(x, C=1):
    """
    PARAMS
    ------
    C: compression factor used to compress
    """
    return torch.exp(x) / C

class STFT(nn.Module):
    def __init__(self, filter_length=1024, hop_length=256, win_length=1024):
        super(STFT, self).__init__()
        
        self.hop_length = hop_length
        self.win_length = win_length
        self.filter_length = filter_length
        
        fft_window = get_window('hann', win_length, fftbins=True)
        fft_window = pad_center(fft_window, filter_length)
        fft_window = torch.from_numpy(fft_window).float()
        self.register_buffer('fft_window', fft_window)
    
    def transform(self, y):
        data = torch.stft(y, n_fft=self.filter_length, hop_length=self.hop_length, 
                                win_length=self.win_length, window=self.fft_window, return_complex=True)
        magnitude = torch.sqrt(data.real**2 + data.imag**2)
        phase = torch.atan2(data.imag, data.real)
        
        return magnitude, phase
    
    def inverse(self, magnitude, phase):

        recombine_magnitude_phase = torch.complex(magnitude*torch.cos(phase), magnitude*torch.sin(phase))
        
        y = torch.istft(recombine_magnitude_phase, n_fft=self.filter_length, hop_length=self.hop_length, 
                    win_length=self.win_length, window=self.fft_window)
        
        return y

class TacotronSTFT(nn.Module):
    def __init__(self, filter_length=1024, hop_length=256, win_length=1024,
                 n_mel_channels=80, sampling_rate=22050, mel_fmin=0.0,
                 mel_fmax=8000.0):
        super(TacotronSTFT, self).__init__()
        
        self.n_mel_channels = n_mel_channels
        self.sampling_rate = sampling_rate
        self.hop_length = hop_length
        self.win_length = win_length
        self.filter_length = filter_length
        
        mel_basis = librosa_mel_fn(
            sampling_rate, filter_length, n_mel_channels, mel_fmin, mel_fmax)
        mel_basis = torch.from_numpy(mel_basis).float()
        self.register_buffer('mel_basis', mel_basis)
        
        self.stft = STFT(filter_length, hop_length, win_length)
    
    def spectral_normalize(self, magnitudes):
        output = dynamic_range_compression(magnitudes)
        return output

    def spectral_de_normalize(self, magnitudes):
        output = dynamic_range_decompression(magnitudes)
        return output

    def mel_spectrogram(self, y):
        """Computes mel-spectrograms from a batch of waves
        PARAMS
        ------
        y: Variable(torch.FloatTensor) with shape (B, T) in range [-1, 1]
        RETURNS
        -------
        mel_output: torch.FloatTensor of shape (B, n_mel_channels, T)
        """
        assert(torch.min(y.data) >= -1)
        assert(torch.max(y.data) <= 1)
                    
        magnitudes, _ = self.stft.transform(y)
    
        mel_output = torch.matmul(self.mel_basis, magnitudes)
        mel_output = self.spectral_normalize(mel_output)
        return mel_output
