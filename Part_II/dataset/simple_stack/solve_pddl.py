import os
import tempfile
import pathlib
from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner
from collections import namedtuple
from .generate_pddl import problem_to_pddl
from . import actions

DOMAIN_FILE = os.path.join(pathlib.Path(__file__).parent.resolve(), 'domain.pddl')



def parse_pyperplan_operator(op):
    def tokenize(chars):
        return chars.replace('(', ' ( ').replace(')', ' ) ').split()
    tokens = tokenize(op.name)
    if tokens[1] == 'stack': # (stack obj oldunder newunder)
        assert(len(tokens) == 6)
        return actions.make_stack(tokens[2], tokens[4])
    elif tokens[1] == 'stackfromtable':
        assert(len(tokens) == 5)
        return actions.make_stack(tokens[2], tokens[3])
    else: # unstack a from b
        assert(len(tokens) == 5)
        assert(tokens[1] == 'unstack')
        return actions.make_unstack(tokens[2])


def solve_pyperplan_pddl(problem_pddl_str):
    '''
    Uses pyperplan to solve a pddl problem
        problem_pddl_str : str
    
    Returns
        [parsed actions] or None
    '''
    search_alg_name = 'bfs'
    heuristic_name = None

    domain_file_name = DOMAIN_FILE
    problem_file = tempfile.NamedTemporaryFile(delete=False)
    with open(problem_file.name, 'w') as f:
        f.write(problem_pddl_str)

    parser = Parser(domain_file_name, problem_file.name)
    
    try: 
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)
        os.remove(problem_file.name)

        # Ground the PDDL
        task = grounding.ground(problem)

        # Get the search alg
        search_alg = planner.SEARCHES[search_alg_name]
        if heuristic_name is None:
            res = search_alg(task)
        else:
            # Get the heuristic
            heuristic = planner.HEURISTICS[heuristic_name](task)

            # Run planning
            res = search_alg(task, heuristic)

    except Exception as e:
        print(e)
        res = None
    # res is a list of 'actions', where each action is a pyperplan Operator
    return [parse_pyperplan_operator(op) for op in res] if res is not None else None

def solve_pddl(init_board, goal_board, view, print_problem=False):
    '''
    pass domain file.
    get problem_to_pddl, write to tempfile
    see hw06.ipynb and mp03.ipynb from 6.s058
    '''
    problem_pddl_str = problem_to_pddl(init_board, goal_board, view)
    if print_problem:
        print(problem_pddl_str)
    return solve_pyperplan_pddl(problem_pddl_str)
        

def test_solve_pddl():
    init_board = {
        ("laptop", "notebook"),
        ("phone", "tv-remote")
    }
    goal_board = {
        ("notebook", "phone", "tv-remote"),
        ("laptop", )
    }
    return solve_pddl(init_board, goal_board)


