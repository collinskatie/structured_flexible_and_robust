from codex.codex import get_completion
from dataset.simple_stack.translate_describer import pddl_describer
from dataset.simple_stack.generate_pddl import predicates_to_pddl
from dataset.simple_stack.solve_pddl import solve_pyperplan_pddl
from dataset.simple_stack import relations
from dataset.simple_stack.generate_state import generate_relations

def codex_planner(init_board, goal_board, view, prompt_path, logger=lambda x,y:None):
    '''
    Returns a list of actions or None
    '''
    
    with open(prompt_path) as f:
        codex_examples = f.read()
        print('Codex examples:')
        print(codex_examples)
    init_prompt = pddl_describer.describe_instance(
                    view = generate_relations(init_board),
                    test = True)
    init_res = '(' + get_completion(
        prompt=codex_examples + init_prompt + '\n(', 
        temperature=0.05,
        stop=';')
    goal_prompt = pddl_describer.describe_instance(
                    view = view,
                    test = True)
    goal_res = '(' + get_completion(
        prompt=codex_examples + goal_prompt + '\n(', 
        temperature=0.05,
        stop=';')
    pddl_problem = predicates_to_pddl(
        init_board = init_board,
        goal_board = goal_board,
        init_predicates = init_res,
        goal_predicates = goal_res
    )
    print('Init prompt')
    print(init_prompt)
    print('init_res')
    print(init_res)
    print('goal prompt')
    print(goal_prompt)
    print('goal res')
    print(goal_res)

    logger('init_prompt', codex_examples + init_prompt)
    logger('init_res', init_res)
    logger('goal_prompt', codex_examples + goal_prompt)
    logger('goal_res', goal_res)

    print('Codex generated pddl problem:')
    print(pddl_problem)

    logger('pddl_problem', pddl_problem)

    plan = solve_pyperplan_pddl(pddl_problem)
    return plan


if __name__ == '__main__':
    init_board = {
        ("laptop", "notebook"),
        ("phone", "tv-remote")
    }
    goal_board = {
        ("notebook", "phone", "tv-remote"),
        ("laptop", )
    }
    view = ( relations.make_bot('laptop'), relations.make_mid('phone', 'notebook'))
    actions = codex_planner(init_board, goal_board, view, prompt_path='dataset/simple_stack/codex_translations/collated.txt')
    print(actions)
