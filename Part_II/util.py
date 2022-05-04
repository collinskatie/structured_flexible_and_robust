import os
import json
import dataset.simple_stack.relations as relations
def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def deserialize_problem(fn):
    with open(fn, 'r') as f:
        d = json.load(f)
        init_board = set(tuple(x) for x in d['init_board'])
        goal_board = set(tuple(x) for x in d['goal_board'])
        remap = d['vocab_map']
        views = d['views']
    return init_board, goal_board, views, remap

    

def deserialize_plan(fn):
    with open(fn, 'r') as nf:
        plan = json.load(nf)

    return [tuple(x) if type(x) is list else x for x in plan]


def board_map(board, fn):
    return set(tuple(fn(x) for x in stack) for stack in board)

def extract_objects(rels):
    objs = set()
    for x in rels:
        relations.map(x, lambda item: objs.add(item))
    return objs
def remap_vocab(init_board, goal_board, views, vocab_map, view):
    if view == 'one':
        return init_board, goal_board, views[view]
    else:
        my_objs = extract_objects(views[view])
        init_objs = extract_objects(views['one'])
        mappable_objs = my_objs - init_objs
        trunc_map = {k: v for k, v in vocab_map.items() if k in mappable_objs}

        mapper = lambda item : trunc_map[item] if item in trunc_map else item

        init_board = board_map(init_board, mapper)
        goal_board = board_map(goal_board, mapper)
        goal_relations = [relations.map(rel, mapper) for rel in views[view]]
    return init_board, goal_board, goal_relations