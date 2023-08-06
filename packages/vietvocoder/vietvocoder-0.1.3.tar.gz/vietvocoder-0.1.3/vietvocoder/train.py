import argparse
import torch

from vietvocoder.model.trainer import Trainer
from vietvocoder.utils.config import Cfg

def train(train_files, test_files, batch_size, device, resume):
    
    config = Cfg.load_config_from_name('waveglow')

    train_config = config['train_config']
    train_config['train_files'] = train_files
    train_config['test_files'] = test_files
    train_config['batch_size'] = batch_size
    train_config['device'] = device

    trainer = Trainer(config)
    if resume:
        trainer.load_checkpoint()

    trainer.train()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_files', required=True, help='foo help')
    parser.add_argument('--test_files', required=True, help='foo help')
    parser.add_argument('--batch_size', default=8, type=int, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--resume', action='store_true')
   
    args = parser.parse_args()

    train(args.train_files, args.test_files, args.batch_size, args.device, args.resume) 
