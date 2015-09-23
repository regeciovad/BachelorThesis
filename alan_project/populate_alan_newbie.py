import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alan_project.settings')

import django
django.setup()

from alan.models import Nonterminal, Terminal, Rule


def populate():
    add_nonterminal('<statement_list>')
    add_nonterminal('<statement>')
    add_nonterminal('<condition>')
    add_nonterminal('<expression>')
    add_nonterminal('<term>')
    add_nonterminal('<factor>')

    add_terminal('i')
    add_terminal('#')
    add_terminal('r')
    add_terminal('+')
    add_terminal('-')
    add_terminal('*')
    add_terminal('/')
    add_terminal('&')
    add_terminal('|')
    add_terminal('!')
    add_terminal('(')
    add_terminal(')')
    add_terminal(';')

    add_rule('<statement_list>', '<statement> ; <statement_list>')
    add_rule('<statement_list>', '<statement>')
    add_rule('<statement>', '<statement> r <condition>')
    add_rule('<statement>', '<statement> & <condition>')
    add_rule('<statement>', '<statement> | <condition>')
    add_rule('<statement>', '<condition>')
    add_rule('<condition>', '! <condition>')
    add_rule('<condition>', '<expression>')
    add_rule('<expression>', '<expression> + <term>')
    add_rule('<expression>', '<expression> - <term>')
    add_rule('<expression>', '<term>')
    add_rule('<term>', '<term> * <factor>')
    add_rule('<term>', '<term> / <factor>')
    add_rule('<term>', '<factor>')
    add_rule('<factor>', '( <expression> )')
    add_rule('<factor>', 'i')
    add_rule('<factor>', '#')

def add_nonterminal(char):
    Nonterminal.objects.get_or_create(char=char)[0]


def add_terminal(char):
    Terminal.objects.get_or_create(char=char)[0]


def add_rule(left_hand_side, right_hand_side):
    Rule.objects.get_or_create(left_hand_side=left_hand_side, right_hand_side=right_hand_side)[0]

if __name__ == '__main__':
    print('Starting Alan population script...')
    populate()
    print('Done')
