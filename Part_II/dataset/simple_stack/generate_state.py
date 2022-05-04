import numpy as np
import json
import dataset.simple_stack.relations as relations

def gen_uniform(vocab, rng=np.random.default_rng()):
    '''
        vocab : set(string)

        returns

        board : set([string]), a set of lists of strings
    '''
    n = len(vocab)
    vocab = sorted(list(vocab))
    if n == 0:
        return []
    if n == 1:
        return [vocab[0]]
    num_partitions = np.ceil(n**0.5).astype('int')
    vocab += [None] * num_partitions
    rng.shuffle(vocab)
    board = set()
    cur = []
    for x in vocab:
        if x is not None:
            cur.append(x)
        else:
            if cur:
                board.add(tuple(cur))
            cur = []
    if cur:
        board.add(tuple(cur))
    return board

def generate_relations(board):
    '''
    Generate all relations on the board.

    Arg:
    board: board

    Return:
    list(Relations)
    '''
    ret = []
    for stack in board:
        ret.append(relations.make_bot(stack[0]))
        for top, bot in zip(stack[1:], stack[:-1]):
            ret.append(relations.make_mid(top, bot))
        ret.append(relations.make_top(stack[-1]))
    return ret
    
