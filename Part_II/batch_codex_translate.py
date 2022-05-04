import json
import argparse
import os
import tempfile
import pathlib
from util import ensure_dir, deserialize_problem, remap_vocab
import numpy as np
from dataset.simple_stack.specs_reader import read_specs
from dataset.simple_stack.evaluate_plan import evaluate_plan
import codex_planner

def plan_problem(problem_fn, rng, id, n, view, prompt_path):
    init_board, goal_board, views, vocab_map = deserialize_problem(problem_fn)
    init_board, goal_board, goal_view = remap_vocab(
        init_board=init_board, 
        goal_board=goal_board, 
        views=views,
        vocab_map=vocab_map,
        view=view)
    print(f'Problem: {init_board} to {goal_board}')
    for i in range(n):
        log_obj = {}
        def logger(x, y):
            log_obj[x] = y
        plan = codex_planner.codex_planner(
            init_board=init_board, 
            goal_board=goal_board, 
            view=goal_view,
            prompt_path=prompt_path,
            logger=logger)
        print(f'PDDL solved plan: {plan}')
        if plan is not None:
            succeed = evaluate_plan(
                init_board=init_board, 
                goal_board=goal_board, 
                view=goal_view, 
                plan=plan)
            if succeed:
                return {
                    'succeed': True,
                    'init_prompt': log_obj.get('init_prompt'),
                    'init_res': log_obj.get('init_res'),
                    'goal_prompt': log_obj.get('goal_prompt'),
                    'goal_res': log_obj.get('goal_res'),
                    'plan': plan
                }
    return {
        'succeed': False,
        'init_prompt': log_obj.get('init_prompt'),
        'init_res': log_obj.get('init_res'),
        'goal_prompt': log_obj.get('goal_prompt'),
        'goal_res': log_obj.get('goal_res'),
        'plan': plan
    }

def main(specs_path, problem_path, output_path, view, prompt_path):
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
                view=view,
                prompt_path=prompt_path
            )
            s.update(tc)
            print(f'succeed: {s["succeed"]}')
            collate.append(s)
    print(f'Succeed: {sum(tc["succeed"] for tc in collate)} / {len(collate)}')
    with open(os.path.join(output_path, 'collated.json'), 'w') as f:
        json.dump(collate, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specs-file', default='dataset/simple_stack/problems.yaml')
    parser.add_argument('--problem-path', default='dataset/simple_stack/problems')
    parser.add_argument('--output-path', default='codex_translations')
    parser.add_argument('--prompt-path', default='dataset/simple_stack/codex_translations/collated.txt')
    parser.add_argument('--view', default='all', choices=['one', 'two', 'all'])
    args = parser.parse_args()
    ensure_dir(args.output_path)
    main(
        specs_path=args.specs_file, 
        problem_path=args.problem_path,
        output_path=args.output_path,
        prompt_path=args.prompt_path,
        view=args.view
    )

