import json
import os
import tempfile
import pathlib
import numpy as np
from dataset.simple_stack.translate_describer import pddl_describer
import argparse
from util import ensure_dir, deserialize_problem, deserialize_plan, remap_vocab
from dataset.simple_stack.specs_reader import read_specs
from dataset.simple_stack.generate_state import generate_relations

def generate_problem_instance(problem_fn, output_fn, test, describer, rng, id, view):
    init_board, goal_board, views, vocab_map = deserialize_problem(problem_fn)
    init_board, goal_board, goal_view = remap_vocab(
        init_board=init_board, 
        goal_board=goal_board, 
        views=views,
        vocab_map=vocab_map,
        view=view)

    s = describer.describe_instance(
        view=generate_relations(init_board),
        test=test, 
        deterministic=True, 
        rng=rng,
        id=id)
    t = describer.describe_instance(
        view=goal_view,
        test=test, 
        deterministic=True, 
        rng=rng,
        id=id)
    with open(output_fn, 'w') as f:
        # f.write(s+'\n\n' + t)
        f.write(s)
    # return s+'\n\n' + t
    return s


def main(specs_path, problem_path, output_path, view):
    with open(specs_path, 'r') as f:
        specs = read_specs(f)
    describer = pddl_describer
    rng = np.random.default_rng(0)
    collate = []
    for tc in specs:
        if not tc['test']:
            s = generate_problem_instance(
                problem_fn=os.path.join(problem_path, tc['name']+'.json'),
                output_fn=os.path.join(output_path, tc['name']+'.txt'),
                test=tc['test'],
                describer=describer,
                rng=rng,
                id=tc['id'],
                view=view
            )
            collate.append(s)
    with open(os.path.join(output_path, 'collated.txt'), 'w') as f:
        f.write('\n\n'.join(collate) + '\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specs-file', default='dataset/simple_stack/problems.yaml')
    parser.add_argument('--problem-path', default='dataset/simple_stack/problems')
    parser.add_argument('--output-path', default='dataset/simple_stack/codex_translations')
    parser.add_argument('--view', default='all', choices=['one', 'two', 'all'])
    args = parser.parse_args()
    ensure_dir(args.output_path)
    main(specs_path=args.specs_file, problem_path=args.problem_path, output_path=args.output_path, view=args.view)

