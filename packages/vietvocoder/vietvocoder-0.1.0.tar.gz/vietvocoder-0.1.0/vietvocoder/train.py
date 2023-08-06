import argparse
import torch

from vietvocoder.model.trainer import Trainer
import vietvocoder.config as cfg

def train(train_files, test_files, batch_size, device, resume):

    trainer = Trainer(
            cfg.data_config,
            cfg.waveglow_config, 
            {**cfg.train_config, 'train_files':train_files, 'test_files':test_files, 
                    'batch_size':batch_size, 'device':device}
            )
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
