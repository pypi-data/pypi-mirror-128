import torch
from torch.utils.data import DataLoader
import os
import numpy as np
import soundfile

from vietvocoder.loader import MelSample
from vietvocoder.model.waveglow import WaveGlow
from vietvocoder.model.layers import WaveGlowLoss
from vietvocoder.utils.logger import Logger
from vietvocoder.utils.download_model import download_weights

class Trainer():
    def __init__(self, config):
        
        data_config = config['data_config']
        train_config = config['train_config']
        waveglow_config = config['waveglow_config']

        trainset = MelSample(train_config['train_files'], **data_config)
        evalset = MelSample(train_config['test_files'], **{**data_config, 'segment_length':64000})
        
        
        batch_size = train_config['batch_size']
        workers = train_config['load_workers']
        self.log_dir = train_config['log_dir']
        self.device = train_config['device']
        self.num_iters = train_config['num_iters']
        self.eval_steps = train_config['eval_steps']
        self.sampling_rate = data_config['sampling_rate']

        self.train_loader = DataLoader(trainset, num_workers=workers, 
                                shuffle=True,
                                batch_size=batch_size,
                                pin_memory=False,
                                drop_last=True)

        self.eval_loader = DataLoader(evalset, num_workers=workers, 
                                shuffle=False,
                                batch_size=batch_size,
                                pin_memory=False,
                                drop_last=True)

        self.train_iter = iter(self.train_loader)

        self.sample_eval_mel, _ = next(iter(self.eval_loader))

        self.model = WaveGlow(**waveglow_config)

        if self.device.startswith('cuda'):
            self.model = self.model.to(self.device)
            self.sample_eval_mel = self.sample_eval_mel.to(self.device)

        self.criterion = WaveGlowLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=train_config['learning_rate'])
        
        pretrained = train_config['pretrained_url']
        if pretrained != None:
            pretrained_weights_path = download_weights(pretrained, md5=train_config['pretrained_md5'])
            self.model.load_state_dict(torch.load(pretrained_weights_path))

        if self.log_dir != None:
            log_name = os.path.join(self.log_dir, 'log.txt')
            self.log = Logger(log_name)
        
        self.best_eval_loss = 99999
        self.current_iter = 0
        
    def train(self):
        for i in range(self.current_iter, self.num_iters):
            self.current_iter = i
            try:
                mel, audio = next(self.train_iter)
            except StopIteration:
                self.train_iter = iter(self.train_loader)
                mel, audio = next(self.train_iter)
            
            loss = self.train_step(mel, audio)
            self.log('iter: {} - train_loss: {}'.format(i, loss))

            if i % self.eval_steps==0:
                eval_loss = self.evaluate()

                if self.log_dir:
                    self.sample()
                if eval_loss < self.best_eval_loss:
                    self.best_eval_loss = eval_loss
                    self.save_checkpoint()

                self.log('iter: {} - valid_loss: {}'.format(i, eval_loss))

    def save_checkpoint(self):
        state = {
	    'iter': self.current_iter,
            'best_eval_loss':self.best_eval_loss,
	    'state_dict': self.model.state_dict(),
	    'optimizer': self.optimizer.state_dict(),
	}

        torch.save(state,os.path.join(self.log_dir, 'checkpoint.pt'))
        torch.save(self.model.state_dict(), os.path.join(self.log_dir, 'model.pt'))

    def load_checkpoint(self):
        state = torch.load(os.path.join(self.log_dir, 'checkpoint.pt'))
        self.current_iter = state['iter']
        self.best_eval_loss = state['best_eval_loss']
        self.model.load_state_dict(state['state_dict'])
        self.optimizer.load_state_dict(state['optimizer'])
        
        print('continue train from the lastest checkpont. current_iter: {}, best_eval_loss: {}'.format(self.current_iter, self.best_eval_loss))

    def train_step(self, mel, audio):
        self.model.train()
        self.model.zero_grad()
    
        mel = mel.to(self.device)
        audio = audio.to(self.device)

        outputs = self.model((mel, audio))

        loss = self.criterion(outputs)

        loss.backward()

        self.optimizer.step()
        
        return loss.item()

    def evaluate(self):
        self.model.eval()
        validation_losses = []
        for batch in self.eval_loader:
            mel, audio = batch
            mel = mel.to(self.device)
            audio = audio.to(self.device)

            with torch.no_grad():
                outputs = self.model((mel, audio))

            loss = self.criterion(outputs) 
            validation_losses.append(loss.item())
        
        return np.mean(validation_losses)

    def sample(self, sigma=1.0):
        sample_audios = self.model.infer(self.sample_eval_mel, sigma=sigma).cpu().numpy()

        for k, sample_audio in enumerate(sample_audios):
            soundfile.write('{}/{:03d}_{:06d}.wav'.format(self.log_dir, k, self.current_iter), sample_audio, self.sampling_rate)
