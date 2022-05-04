import numpy as np
from functools import partial
from gpt.openai_gpt3 import get_gpt_completion as gpt3_completion
from gpt.openai_gpt3 import get_codex_completion as codex_completion
# from codex.codex import get_completion as codex_completion
from dataset.simple_stack.describer import nl_describer, python_describer
from dataset.simple_stack.parser import nl_plan_parser, python_plan_parser


def lm_planner(init_board, goal_board, lm_type, engine_type, view, prompt_path, logger=lambda x,y:None):
    '''
    Args:
    - init_board : board
    - goal_board : board
    - lm_type : "nl" or "codex" # this branch deprecates "lm_type=codex", 
        so we're ignoring this fied
    - engine_type : "codex", "gpt3", "gptneo"

    Returns:
    [action]
    '''
    if engine_type == 'gptneo':
        import gpt.gpt
        gptneo_completion = gpt.gpt.get_completion
    else:
        gptneo_completion = lambda x: x
    assert(lm_type == 'nl')
    engine_map = {
        'codex': partial(codex_completion, stop='Initially:', temperature=0.05),
        'gpt3': partial(gpt3_completion, stop='Initially:', temperature=0.05),
        'gptneo': partial(gptneo_completion, stop='Initially:', temperature=0.05),
    }
    describer_map = {
        'nl': nl_describer,
        'python': python_describer
    }

    
    with open(prompt_path) as f:
        examples = f.read()

    parser_map = {
        'nl': nl_plan_parser,
        'python': python_plan_parser
    }
    get_completion = engine_map[engine_type]
    describer = describer_map[lm_type]
    parser = parser_map[lm_type]

    problem_prompt = describer.describe_instance(
        init_board=init_board, 
        goal_board=goal_board, 
        view=view,
        plan=None, 
        test=True, 
        deterministic=True, 
        rng=np.random.default_rng(), 
        id=None
    )
    plan = get_completion(
        prompt=examples + problem_prompt)
        
    print('LM Query:')
    print(examples + problem_prompt)
    logger('query', examples + problem_prompt)
    print('LM Plan:')
    logger('plan', plan)
    print(plan)
    parsed = parser.parse(plan)
    return parsed
    
    