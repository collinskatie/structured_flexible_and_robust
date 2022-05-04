import json
import argparse
import os
import tempfile
import pathlib
import numpy as np
from dataset.simple_stack.specs_reader import read_specs
from dataset.simple_stack.evaluate_plan import evaluate_plan
import lm_planner
from util import ensure_dir, deserialize_problem, remap_vocab
from collections import defaultdict


def plan_problem(problem_fn, rng, id, n, lm_type, prompt_path, engine_type, view):
    init_board, goal_board, views, vocab_map = deserialize_problem(problem_fn)
    init_board, goal_board, goal_view = remap_vocab(
        init_board=init_board, 
        goal_board=goal_board, 
        views=views,
        vocab_map=vocab_map,
        view=view)
    print(f'Problem: {init_board} to {views[view]}')
    log_obj = {}
    for i in range(n):
        log_obj = {}
        def logger(x, y):
            log_obj[x] = y
        plan = lm_planner.lm_planner(
            init_board=init_board, 
            goal_board=goal_board,
            view=goal_view,
            lm_type=lm_type,
            prompt_path=prompt_path,
            engine_type=engine_type,
            logger=logger
        )
        print('Parsed LM plan:')
        print(plan)
        if plan is not None:
            succeed = evaluate_plan(init_board, goal_board, goal_view, plan)
            print(f'Succeed {succeed}')
            if succeed:
                return {
                    'succeed': True,
                    'query': log_obj.get('query'),
                    'lm_plan': log_obj.get('plan'), 
                    'parsed_plan': plan
                }
    return {
        'succeed': False,
        'query': log_obj.get('query'),
        'lm_plan': log_obj.get('plan'),
        'parsed_plan': plan
    }

def main(specs_path, problem_path, output_path, lm_type, prompt_path, view, engine_type):
    with open(specs_path, 'r') as f:
        specs = read_specs(f)
    rng = np.random.default_rng(0)
    collate = []
    for tc in specs:
        if tc['test']:
            print(f'\n\nTesting {tc["name"]}')
            s = plan_problem(
                problem_fn=os.path.join(problem_path, tc['name']+'.json'),
                rng=rng,
                id=tc['id'],
                n=1,
                lm_type=lm_type,
                prompt_path=prompt_path,
                engine_type=engine_type,
                view=view
            )
            s.update(tc)
            collate.append(s)
    print(f'{view} succeed: {sum(tc["succeed"] for tc in collate)} / {len(collate)}')
    with open(os.path.join(output_path, 'collated.json'), 'w') as f:
        json.dump(collate, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specs-file', default='dataset/simple_stack/problems.yaml')
    parser.add_argument('--problem-path', default='dataset/simple_stack/problems')
    parser.add_argument('--output-path', default='nl_plans')
    parser.add_argument('--output-type', default='nl', choices=['nl', 'python'])
    parser.add_argument('--prompt-path', default='dataset/simple_stack/gpt3_prompts/collated.txt')
    parser.add_argument('--engine-type', default='gptneo', choices=['gptneo', 'gpt3', 'codex'])
    parser.add_argument('--view', default='all', choices=['one', 'two', 'all'])
    args = parser.parse_args()
    ensure_dir(args.output_path)
    main(
        specs_path=args.specs_file, 
        problem_path=args.problem_path,
        output_path=args.output_path,
        lm_type=args.output_type,
        prompt_path=args.prompt_path,
        engine_type=args.engine_type,
        view=args.view
    )

