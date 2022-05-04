import json
import numpy as np
from . import actions
import os
import pathlib
from . import relations
from .generate_state import generate_relations

'''
Exports:
- nl_describer
- python_describer (DEPRECATED ON THIS BRANCH)
'''


PYTHON_TEST_TEMPLATE = r'''
"""
There are some items stacked on the table. You can either
1. Stack the topmost item on the top of another stack, or
2. Unstack the topmost item of a stack and place it on the table

Initially:
{py_init}


Goal:
{py_goal}

Actions:
"""
'''

PYTHON_TEMPLATE = r'''
"""
There are some items stacked on the table. You can either
1. Stack the topmost item on the top of another stack, or
2. Unstack the topmost item of a stack and place it on the table

Initially:
{py_init}


Goal:
{py_goal}

Actions:
"""
{py_plan}
'''

NL_PREAMBLE = \
r'''There are some items stacked on the table. You can perform either of the following actions:
1. Move the topmost item of a stack to the top of another stack, or
2. Unstack the topmost item of a stack and place it on the table

Given an initial configuration and a set of goal requirements, output a series of actions that satisfies the goal requirements'''

NL_TEST_TEMPLATE = r'''Initially:
{init}

Goal:
{goal}

Actions:
'''

NL_TEMPLATE = r'''Initially:
{init}

Goal:
{goal}

Actions:
{plan}
'''



def read_templates(fn):
    with open(fn, "r") as f:
        return json.load(f)


def sanitize_board(board, sanitizer):
    '''
    Args:
        - board : Board
        - sanitizer : str -> str
    Returns:
        - board : Board
    '''
    return set(tuple(sanitizer(x) for x in stack) for stack in board)

class Describer:
    def __init__(self, PLAN_TEMPLATES_FILE, STACK_TEMPLATES_FILE):
        self.PLAN_TEMPLATES = read_templates(PLAN_TEMPLATES_FILE)
        self.STACK_TEMPLATES = read_templates(STACK_TEMPLATES_FILE)
    
    def sanitize(self, word):
        return word

    def describe_action(self, action, deterministic, rng=np.random.default_rng()):
        if actions.action_type(action) == actions.STACK:
            top = self.sanitize(actions.get_stack_top(action))
            bot = self.sanitize(actions.get_stack_bottom(action))
            return (self.PLAN_TEMPLATES['stack'][0] if deterministic 
                else rng.choice(self.PLAN_TEMPLATES['stack'])).format(top, bot)
        else:
            obj = self.sanitize(actions.get_unstack_obj(action))
            return (self.PLAN_TEMPLATES['unstack'][0] if deterministic
                else rng.choice(self.PLAN_TEMPLATES['unstack'])).format(obj)

    def describe_plan(self, plan, deterministic, rng=np.random.default_rng()):
        '''
        Args:
            - plan : [action].  See actions.py

        Returns:
            - nl_plan : [string]
        '''
        return [
            self.describe_action(action, deterministic, rng) for action in plan
        ]
    

    def describe_view(self, view, deterministic, rng=np.random.default_rng()):
        view = [relations.map(rel, self.sanitize) for rel in view]
        desc = [
            relations.switch(rel, {
                relations.BOT_REL: lambda rel: self.STACK_TEMPLATES['bot'][0].format(relations.top(rel)),
                relations.TOP_REL: lambda rel: self.STACK_TEMPLATES['top'][0].format(relations.bot(rel)),
                relations.MID_REL: lambda rel: self.STACK_TEMPLATES['mid'][0].format(relations.bot(rel), relations.top(rel))
            }) for rel in view
        ]
        return '\n'.join(desc)
        

TDIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'describer_templates')

class NLDescriber(Describer):
    def __init__(self):
        nl_plans = os.path.join(TDIR, 'nl_plans.json')
        nl_stacks = os.path.join(TDIR, 'nl_stacks.json')
        super().__init__(nl_plans, nl_stacks)
        self.preamble = NL_PREAMBLE
    def sanitize(self, word):
        return word.replace('-', ' ')
    def describe_instance(self, init_board, goal_board, view, plan, test=False, deterministic=True, rng=np.random.default_rng(), id=None):
        nl_init = self.describe_view(generate_relations(init_board), deterministic, rng)
        nl_goal = self.describe_view(view, deterministic, rng)
        if not test:
            nl_plan = '\n'.join(self.describe_plan(plan, deterministic, rng))
        if test:
            s = NL_TEST_TEMPLATE.format(init=nl_init, goal=nl_goal)
        else:
            s = NL_TEMPLATE.format(init=nl_init, goal=nl_goal, plan=nl_plan)
        return s



class PythonDescriber(Describer):
    def __init__(self):
        plans = os.path.join(TDIR, 'python_plans.json')
        stacks = os.path.join(TDIR, 'python_stacks.json')
        super().__init__(plans, stacks)
    def sanitize(self, word):
        '''
        Args:
            - word : str
        Returns:
            - sanitized : str
        '''
        return word.replace('-', '_').replace(' ', '_')
    def describe_instance(self, init_board, goal_board, plan, test=False, deterministic=True, rng=np.random.default_rng(), id=0):
        py_init = self.describe_board(init_board, deterministic, rng)
        py_goal = self.describe_board(goal_board, deterministic, rng)
        if not test:
            py_plan = self.describe_plan(plan, deterministic, rng)
            py_plan = '\n'.join(py_plan)
        if test:
            s = PYTHON_TEST_TEMPLATE.format(py_init=py_init, py_goal=py_goal)
        else:
            s = PYTHON_TEMPLATE.format(py_init=py_init, py_goal=py_goal, py_plan=py_plan)
        return s


nl_describer = NLDescriber()
python_describer = PythonDescriber()







            