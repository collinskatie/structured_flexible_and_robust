import json
import os
import tempfile
import pathlib
import argparse
import numpy as np
from dataset.simple_stack.describer import nl_describer, python_describer
from dataset.simple_stack.translate_describer import pddl_describer
from dataset.simple_stack.specs_reader import read_specs
from dataset.simple_stack.solve_pddl import solve_pddl
from util import ensure_dir, deserialize_problem, deserialize_plan, remap_vocab


def plan_and_save(init_board, goal_board, view, plan_fn):
    actions = solve_pddl(init_board, goal_board, view)
    with open(plan_fn, 'w') as f:
        json.dump(actions, f)

def generate_problem_instance(plan_fn, problem_fn, output_fn, test, describer, rng, id, view):
    init_board, goal_board, views, vocab_map = deserialize_problem(problem_fn)
    init_board, goal_board, goal_view = remap_vocab(
        init_board=init_board, 
        goal_board=goal_board, 
        views=views,
        vocab_map=vocab_map,
        view=view)

    plan_and_save(init_board, goal_board, goal_view, plan_fn)
    plan = deserialize_plan(plan_fn)
    s = describer.describe_instance(
        init_board=init_board, 
        goal_board=goal_board,
        view=goal_view,
        plan=plan, 
        test=test, 
        deterministic=True, 
        rng=rng,
        id=id)
    with open(output_fn, 'w') as f:
        f.write(s)
    return s


def main(specs_path, plan_path, problem_path, output_path, output_type, view):
    with open(specs_path, 'r') as f:
        specs = read_specs(f)
    d_map = {
        'python': python_describer,
        'nl': nl_describer
    } 
    describer = d_map[output_type]
    rng = np.random.default_rng(0)
    collate = [describer.preamble]
    for tc in specs:
        if not tc['test']:
            s = generate_problem_instance(
                os.path.join(plan_path, tc['name']+'.json'),
                os.path.join(problem_path, tc['name']+'.json'),
                os.path.join(output_path, tc['name']+'.txt'),
                tc['test'],
                describer,
                rng,
                tc['id'],
                view=view
            )
            collate.append(s)
    with open(os.path.join(output_path, 'collated.txt'), 'w') as f:
        f.write('\n\n'.join(collate) + '\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specs-file', default='dataset/simple_stack/problems.yaml')
    parser.add_argument('--plan-path', default='dataset/simple_stack/plans')
    parser.add_argument('--problem-path', default='dataset/simple_stack/problems')
    parser.add_argument('--output-path', default='dataset/simple_stack/gpt3_prompts')
    parser.add_argument('--output-type', default='nl', choices=['nl', 'python'])
    parser.add_argument('--view', default='all', choices=['one', 'two', 'all'])
    args = parser.parse_args()
    ensure_dir(args.plan_path)
    ensure_dir(args.output_path)
    main(args.specs_file, args.plan_path, args.problem_path, args.output_path, args.output_type, args.view)

