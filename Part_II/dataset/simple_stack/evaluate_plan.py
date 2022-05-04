from collections import defaultdict
from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner
import numpy as np
import pathlib
import os
import tempfile
from .solve_pddl import parse_pyperplan_operator
from .generate_pddl import problem_to_pddl
from .actions import sanitize_action
from . import relations

DOMAIN_FILE = os.path.join(pathlib.Path(__file__).parent.resolve(), 'domain.pddl')


def evaluate_plan(init_board, goal_board, view, plan, forgive_invalid_action=True):
    '''
    Args:
    - init_board, goal_board
    - plan : [action]
    
    Returns:
    - succeed : Bool
    '''
    plan = [sanitize_action(action, lambda x: x.replace(' ', '-')) for action in plan]
    problem_pddl_str = problem_to_pddl(init_board, goal_board, view)
    
    problem_file = tempfile.NamedTemporaryFile(delete=False)
    with open(problem_file.name, 'w') as f:
        f.write(problem_pddl_str)

    domain_file_name = DOMAIN_FILE

    parser = Parser(domain_file_name, problem_file.name)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    os.remove(problem_file.name)

    # Ground the PDDL
    task = grounding.ground(problem)
    
    operator_map = defaultdict(list)
    for op in task.operators:
        operator_map[parse_pyperplan_operator(op)].append(op)
    state = task.initial_state
    # print(state)
    for action in plan:
        if action not in operator_map:
            # invalid action
            print(f'action {action} not found')
            if forgive_invalid_action:
                continue
            else:
                return False
        else:
            valid_ops = [op for op in operator_map[action] if op.applicable(state)]
            if len(valid_ops) == 0:
                # invalid action
                # print(action)
                # print(operator_map[action])
                # print(valid_ops)
                print(f'operator {action} not applicable')
                if forgive_invalid_action:
                    continue
                else:
                    return False
            elif len(valid_ops) > 1:
                print(valid_ops)
                print(state)
                print(action)
                raise Exception('more than one applicable operator!!')
            else:
                state = valid_ops[0].apply(state)
    if task.goal_reached(state):
        return True
    else:
        print('goal state not reached')
        return False
        



def test_evaluate_plan():
    init_board = {
        ("laptop", "notebook"),
        ("phone", "tv-remote")
    }
    goal_board = {
        ("notebook", "phone", "tv-remote"),
        ("laptop", )
    }
    view = ( relations.make_bot('laptop'), relations.make_mid('phone', 'notebook'))
    bad_plan = ["laptop", ("phone", "tv-remote")]
    good_plan = ["notebook", "tv-remote", ("phone", "notebook"), ("tv-remote", "phone")]
    assert(evaluate_plan(init_board, goal_board, view, bad_plan) == False)
    assert(evaluate_plan(init_board, goal_board, view, good_plan) == True)


if __name__ == '__main__':
    print(test_evaluate_plan())

    

    

