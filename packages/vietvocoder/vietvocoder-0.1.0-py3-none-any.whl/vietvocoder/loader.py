import torch
from torch.utils.data import Dataset
from scipy.io import wavfile
import numpy as np

from vietvocoder.stft import TacotronSTFT

MAX_WAV_VALUE = 32768.0

def load_txt(fname):
    with open(fname, 'r') as f:
        files = f.readlines()
    
    files = [f.rstrip() for f in files]
    return files

def load_audio(fname):
    sampling_rate, audio = wavfile.read(fname)
    audio = torch.from_numpy(audio.copy()).float()
    
    return sampling_rate, audio

class MelSample(Dataset):
    def __init__(self, dataset, segment_length, filter_length, hop_length, 
                 win_length, n_mel_channels, sampling_rate, mel_fmin, mel_fmax):
        
        self.dataset = load_txt(dataset)
        np.random.shuffle(self.dataset)
        
        self.segment_length = segment_length
        self.sampling_rate = sampling_rate
        
        self.stft = TacotronSTFT(filter_length=filter_length, hop_length=hop_length, 
                                 win_length=win_length, n_mel_channels=n_mel_channels, 
                                 sampling_rate=sampling_rate, 
                                 mel_fmin=mel_fmin, mel_fmax=mel_fmax)
                
    def __len__(self):
        return len(self.dataset)
    
    def get_mel(self, audio):
        audio = audio.unsqueeze(0)
        mel = self.stft.mel_spectrogram(audio)
        mel = mel.squeeze(0)
        
        return mel
    
    def __getitem__(self, index):
        fname = self.dataset[index]
        sampling_rate, audio = load_audio(fname)

        if sampling_rate != self.sampling_rate:
            raise ValueError("Current {} SR doesn't match target {} SR".format(sampling_rate, self.sampling_rate))
        
        if len(audio) > self.segment_length:
            max_start = len(audio) - self.segment_length
            start = np.random.randint(0, max_start)          
            audio = audio[start:start+self.segment_length]
        else:
            raise ValueError('Segment length must be shorter than audio size')
            
        audio = audio/MAX_WAV_VALUE
        mel = self.get_mel(audio)
        return (mel, audio)
