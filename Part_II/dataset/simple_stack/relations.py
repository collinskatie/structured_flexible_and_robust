from collections import namedtuple
BOT_REL = 'bot'
TOP_REL = 'top'
MID_REL = 'mid'

# Relation = namedtuple('Relation', ['type', 'top', 'bot'])


# relations are tuples: type, top, bot
def rel_type(relation):
    return relation[0]

def bot(rel):
    return rel[2]

def top(rel):
    return rel[1]

def make_bot(x):
    return (BOT_REL, x, None)

def make_mid(top, bot):
    return (MID_REL, top, bot)

def make_top(x):
    return (TOP_REL, None, x)

def map(rel, fn):
    return (
        rel[0], 
        rel[1] if rel[1] is None else fn(rel[1]), 
        rel[2] if rel[2] is None else fn(rel[2])
    )
def switch(rel, fmap):
    return fmap[rel[0]](rel)