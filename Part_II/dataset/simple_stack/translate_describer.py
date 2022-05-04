import json
import numpy as np
import os
import pathlib
from . import actions
from . import relations
from .describer import nl_describer

'''
Exports:
- pddl_describer
'''

pddl_instance_template = \
'''
{nl_board}
{pddl_board}
'''
pddl_test_instance_template = \
'''
{nl_board}
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

class PDDLDescriber:
    def __init__(self):
        STACK_TEMPLATES_FILE = os.path.join(TDIR, 'pddl_stacks.json')
        self.STACK_TEMPLATES = read_templates(STACK_TEMPLATES_FILE)
    
    def sanitize(self, word):
        return word.replace(' ', '-')


    def describe_view(self, view, deterministic, rng=np.random.default_rng()):
        '''
            view: [relations]

            returns

            desc : string
        '''
        
        view = [relations.map(rel, self.sanitize) for rel in view]
        desc = [
            relations.switch(rel, {
                relations.BOT_REL: lambda rel: self.STACK_TEMPLATES['bot'][0].format(relations.top(rel)),
                relations.TOP_REL: lambda rel: self.STACK_TEMPLATES['top'][0].format(relations.bot(rel)),
                relations.MID_REL: lambda rel: self.STACK_TEMPLATES['mid'][0].format(relations.bot(rel), relations.top(rel))
            }) for rel in view
        ]
        return "\n".join(desc)
    
    def describe_instance(self, view, test=False, deterministic=True, rng=np.random.default_rng(), id=None):
        nl_board = ';'+nl_describer.describe_view(view=view, deterministic=deterministic, rng=rng).replace('\n', '\n;')
        pddl_board = self.describe_view(view=view, deterministic=deterministic, rng=rng)
        if test:
            return nl_board
        else:
            return nl_board + '\n' + pddl_board
        return s



TDIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'describer_templates')

pddl_describer = PDDLDescriber()

if __name__ == '__main__':
    view = ( relations.make_bot('laptop'), relations.make_mid('phone', 'notebook'))
    print('test')
    print(pddl_describer.describe_instance(view, test=True))
    print('not test')
    print(pddl_describer.describe_instance(view, test=False))





            