from . import relations

def board_to_predicates(board):
    '''
    Args:
        board : set([string])

    Returns:
        predicates : [string]
    '''
    predicates = []
    for stack in board:
        predicates.append(f"(ontable {stack[0]})")
        for s1, s2 in zip(stack[1:], stack[:-1]):
            predicates.append(f"(on {s1} {s2})")
        predicates.append(f"(clear {stack[-1]})")
    return predicates

def view_to_predicates(view):
    def translate(rel):
        if relations.rel_type(rel) == relations.BOT_REL:
            return f"(ontable {relations.top(rel)})"
        elif relations.rel_type(rel) == relations.TOP_REL:
            return f"(clear {relations.bot(rel)})"
        else:
            return f"(on {relations.top(rel)} {relations.bot(rel)})"
    return [
        translate(rel) for rel in view
    ]

def sanitize_vocab(name):
    return name.replace(' ', '-')

def sanitize_board(board):
    return set(tuple(sanitize_vocab(name) for name in stack) for stack in board)

def sanitize_view(view):
    return [relations.map(rel, sanitize_vocab) for rel in view]

def gen_noteq_predicates(objects):
    return [
        f'(noteq {obj1} {obj2})'
        for obj1 in objects
            for obj2 in objects
                if obj1 != obj2
    ]
def predicates_to_pddl(init_board, goal_board, init_predicates, goal_predicates):
    '''
    Generate a pddl problem for getting from init_predicates to goal_predicates
    Meant for use by the codex LOT planner
    '''
    init_board = sanitize_board(init_board)
    goal_board = sanitize_board(goal_board)
    
    objects = sorted([obj for stack in init_board for obj in stack])
    goal_objects = sorted([obj for stack in goal_board for obj in stack])
    assert(objects == goal_objects)

    noteq_predicates = gen_noteq_predicates(objects)
    
    object_str = "(:objects " + ' '.join(objects) + ")"
    init_str = "(:init " + init_predicates + " " + ' '.join(noteq_predicates)  + ")"
    goal_str = "(:goal (and " + goal_predicates + "))"

    problem_str = \
    f"""
    (define (problem gen-problem)
        (:domain simple-blocks)
        {object_str}
        {init_str}
        {goal_str}
    )
    """
    return problem_str

def problem_to_pddl(init_board, goal_board, view):
    init_board = sanitize_board(init_board)
    goal_board = sanitize_board(goal_board)
    view = sanitize_view(view)
    
    objects = sorted([obj for stack in init_board for obj in stack])
    goal_objects = sorted([obj for stack in goal_board for obj in stack])
    assert(objects == goal_objects)
    

    init_predicates = board_to_predicates(init_board)
    goal_predicates = view_to_predicates(view)

    noteq_predicates = gen_noteq_predicates(objects)

    object_str = "(:objects " + ' '.join(objects) + ")"
    init_str = "(:init " + " ".join(init_predicates + noteq_predicates) +  ")"
    goal_str = "(:goal (and " + ' '.join(goal_predicates) + "))"

    problem_str = \
    f"""
    (define (problem gen-problem)
        (:domain simple-blocks)
        {object_str}
        {init_str}
        {goal_str}
    )
    """
    return problem_str

def test_problem_to_pddl():
    init_board = {
        ("laptop", "notebook"),
        ("phone", "tv-remote")
    }
    goal_board = {
        ("notebook", "phone", "tv-remote"),
        ("laptop", )
    }

    view = ( relations.make_bot('laptop'), relations.make_mid('phone', 'notebook'))
    return problem_to_pddl(init_board, goal_board, view)
