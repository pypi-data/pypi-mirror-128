import argparse
import numpy as np
import soundfile
import torch

from vietvocoder.model.predictor import Predictor
import vietvocoder.config as cfg

def predict(mel_file, model_weights, out_file, device):
    mel = np.load(mel_file)

    predictor = Predictor(cfg.waveglow_config, cfg.data_config, model_weights, device)
    audio = predictor.predict(mel)
    soundfile.write(out_file, audio, cfg.data_config['sampling_rate'])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mel_file', required=True, help='foo help')
    parser.add_argument('--weights', required=True, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--out_file', default='out.wav', help='foo help')

    args = parser.parse_args()

    predict(args.mel_file, args.weights, args.out_file, args.device)
