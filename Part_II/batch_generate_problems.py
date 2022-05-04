import json
import os
import tempfile
import pathlib
import numpy as np
import argparse
import dataset.simple_stack.generate_state as generate_state

from dataset.simple_stack.specs_reader import read_specs


def main(specs, problem_path, vocab_file, complex_vocab_file):
    with open(vocab_file, 'r') as f:
        vocab = sorted(json.load(f))
    with open(complex_vocab_file, 'r') as f:
        complex_vocab = sorted(json.load(f))
    rng = np.random.default_rng(0)
    for tc in specs:
        subvocab = set(rng.choice(vocab, size=tc['num_obj'], replace=False))
        subcomplex_vocab = rng.choice(complex_vocab, size=tc['num_obj'], replace=False).tolist()
        vocab_map = {
            simple: comp
            for simple, comp in zip(subvocab, subcomplex_vocab)
        }
        init_board = generate_state.gen_uniform(subvocab, rng)
        goal_board = generate_state.gen_uniform(subvocab, rng)
        file_name = os.path.join(problem_path, tc['name'] + '.json')
        relations = generate_state.generate_relations(goal_board)
        num_relations = len(relations)
        relations_perm = rng.permutation(relations).tolist()
        views = {
            'one': relations_perm[:1],
            'two': relations_perm[:2],
            'all': relations_perm
        }
        with open(file_name, 'w') as f:
            json.dump({
                'init_board': list(init_board), 
                'goal_board': list(goal_board),
                'views': views,
                'vocab_map': vocab_map
            }, f, sort_keys=True, indent=4)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specs-file', default='dataset/simple_stack/problems.yaml')
    parser.add_argument('--vocab-file', default='dataset/simple_stack/vocab.json')
    parser.add_argument('--complex-vocab-file', default='dataset/simple_stack/vocab_complex.json')
    parser.add_argument('--problem-path', default='dataset/simple_stack/problems')
    args = parser.parse_args()
    with open(args.specs_file, 'r') as f:
        main(specs=read_specs(f), 
            vocab_file=args.vocab_file, 
            complex_vocab_file=args.complex_vocab_file,
            problem_path=args.problem_path)

