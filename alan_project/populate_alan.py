import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alan_project.settings')

import django
django.setup()

from alan.models import *

def populate():
    enon = add_nonterminal('E')
    fnon = add_nonterminal('F')
    tnon = add_nonterminal('T')
    
    iterm = add_terminal('i')
    plusterm = add_terminal('+')
    timesterm = add_terminal('*')
    beginterm = add_terminal('(')
    endterm = add_terminal(')')
    
    first = add_rule('E', 'E+T')
    second = add_rule('E', 'T')
    third = add_rule('T', 'T*F')
    fourth = add_rule('T', 'F')
    fifth = add_rule('F', '(E)')
    sixth = add_rule('F', 'i')
    
    
def add_nonterminal(char):
    n = Nonterminal.objects.get_or_create(char=char)[0]
    return n

def add_terminal(char):
    t = Terminal.objects.get_or_create(char=char)[0]
    return t

def add_rule(left_side, right_side):
    r = Rule.objects.get_or_create(left_side=left_side, right_side=right_side)[0]
    return r


if __name__ == '__main__':
    print ('Starting Alan population script...')
    populate()
    print ('Done')