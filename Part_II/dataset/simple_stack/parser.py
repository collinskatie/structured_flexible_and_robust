import json
import numpy as np
from . import actions
import os
import pathlib
import re

'''
exports nl_plan_parser, python_plan_parser
'''

TDIR = os.path.join(pathlib.Path(__file__).parent.resolve(), 'describer_templates')

def read_templates(fn):
    with open(fn, "r") as f:
        return json.load(f)

class NLPlanParser:
    def __init__(self):
        PLAN_TEMPLATES_FILE = os.path.join(TDIR, 'nl_plans.json')
        self.PLAN_TEMPLATES = read_templates(PLAN_TEMPLATES_FILE)
    def segmenter(self, plan):
        '''
        Args:
        plan : str

        Returns:
        plan : [action]
        '''
        return [s.strip() for s in plan.split('\n')]
    def parseAction(self, tp, action_str):
        '''
        Args:
        tp : 'stack' or 'unstack'
        action_str : str

        Returns:
        action or None
        '''
        for template in self.PLAN_TEMPLATES[tp]:
            match = re.fullmatch(template.replace('.', r'\.').format(*['(.+)']*3), action_str) 
            if match is not None:
                if tp == 'stack':
                    return actions.make_stack(*match.group(1, 2))
                else:
                    return actions.make_unstack(match.group(1))
        return None


    def parse(self, plan):
        '''
        Args:
        plan : str

        Returns:
        plan : [action] or None
        '''
        plan  = self.segmenter(plan)
        final_plan = []
        for action in plan:
            stack = self.parseAction('stack', action)
            unstack = self.parseAction('unstack', action)

            if stack is None and unstack is None:
                continue # ignore malformed
            elif stack is not None and unstack is not None:
                # prioritize unstack
                final_plan.append(unstack)
            else:
                final_plan.append(unstack if stack is None else stack)
        return final_plan
        


class PythonPlanParser:
    def __init__(self):
        PLAN_TEMPLATES_FILE = os.path.join(TDIR, 'python_plans.json')
        self.PLAN_TEMPLATES = read_templates(PLAN_TEMPLATES_FILE)
    def segmenter(self, plan):
        '''
        Args:
        plan : str

        Returns:
        plan : [action]
        '''
        return [s.strip() for s in plan.split('\n')]
    def parseAction(self, tp, action_str):
        '''
        Args:
        tp : 'stack' or 'unstack'
        action_str : str

        Returns:
        action or None
        '''
        for template in self.PLAN_TEMPLATES[tp]:
            match = re.fullmatch(template.replace('.', r'\.').replace('(', r'\(').replace(')', r'\)').format(*['(.+)']*3), action_str) 
            if match is not None:
                if tp == 'stack':
                    return actions.make_stack(*match.group(1, 2))
                else:
                    return actions.make_unstack(match.group(1))
        return None


    def parse(self, plan):
        '''
        Args:
        plan : str

        Returns:
        plan : [action] or None
        '''
        plan  = self.segmenter(plan)
        final_plan = []
        for action in plan:
            stack = self.parseAction('stack', action)
            unstack = self.parseAction('unstack', action)

            if stack is None and unstack is None:
                continue # ignore malformed
            elif stack is not None and unstack is not None:
                raise Exception("Ambiguous parsing of plan")
            else:
                final_plan.append(unstack if stack is None else stack)
        return final_plan

nl_plan_parser = NLPlanParser()
python_plan_parser = PythonPlanParser()

def test_NL_plan_parser():
    parser = NLPlanParser()
    parsed = parser.parse('Move the alarm-clock onto the table.\nMove the phone onto the table.\nStack the alarm-clock on top of the phone.')
    assert(parsed == ['alarm-clock', 'phone', ('alarm-clock', 'phone')])
def test_python_plan_parser():
    parser = PythonPlanParser()
    plan = r'''
    unstack(notebook)
    unstack(alarm_clock)
    stack(speaker, notebook)
    return
    '''
    assert parser.parse(plan) == ['notebook', 'alarm_clock', ('speaker', 'notebook')]
if __name__ == '__main__':
    print(test_NL_plan_parser())
    print(test_python_plan_parser())
    print('test good')
        