import argparse
import numpy as np

from vietvoice.model.predictor import Predictor
from vietvoice.utils.config import Cfg

from vietvoice.vitext_to_phoneme import vitext_clean, vitext_to_phoneme

def predict(text, weights, out_file, device):
    config = Cfg.load_config_from_name('tacotron2_vi_phoneme')

    predictor = Predictor(config, weights=weights, device=device)
    
    text = vitext_clean(text)
    print('clean text: {}'.format(text))
    phoneme = vitext_to_phoneme(text)
    print('phoneme: {}'.format(phoneme))

    mel = predictor.predict(phoneme)
    
    np.save(args.out_file, mel)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True, help='foo help')
    parser.add_argument('--weights', required=True, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--out_file', default='out.npy', help='foo help')

    args = parser.parse_args()

    predict(args.text, args.weights, args.out_file, args.device)
