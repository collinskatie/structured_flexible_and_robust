'''
    interface for actions
'''

STACK = 0
UNSTACK = 1

def make_stack(a, b):
    return (a, b)

def make_unstack(a):
    return a

def action_type(o):
    if type(o) is tuple:
        return STACK
    else:
        return UNSTACK

def get_stack_top(o):
    assert(action_type(o) == STACK)
    return o[0]
def get_stack_bottom(o):
    assert(action_type(o) == STACK)
    return o[1]

def get_unstack_obj(o):
    assert(action_type(o) == UNSTACK)
    return o
def sanitize_action(o, sanitizer):
    if action_type(o) == STACK:
        return make_stack(sanitizer(get_stack_top(o)), sanitizer(get_stack_bottom(o)))
    else:
        return make_unstack(sanitizer(get_unstack_obj(o)))