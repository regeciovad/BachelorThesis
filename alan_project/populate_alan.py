import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alan_project.settings')

import django
django.setup()

from alan.models import Nonterminal, Terminal, Rule


def populate():
    add_nonterminal('<program>')
    add_nonterminal('<declaration part>')
    add_nonterminal('<declaration list>')
    add_nonterminal('<declaration>')
    add_nonterminal('<variable list>')
    add_nonterminal('<execution part>')
    add_nonterminal('<statement list>')
    add_nonterminal('<statement>')
    add_nonterminal('<input list>')
    add_nonterminal('<output list>')
    add_nonterminal('<write member>')
    add_nonterminal('<condition>')
    add_nonterminal('<expression>')
    add_nonterminal('<term>')
    add_nonterminal('<factor>')

    add_terminal('i')
    add_terminal('t')
    add_terminal('#')
    add_terminal('r')
    add_terminal('+')
    add_terminal('-')
    add_terminal('*')
    add_terminal('/')
    add_terminal('&')
    add_terminal('|')
    add_terminal('!')
    add_terminal(',')
    add_terminal(';')
    add_terminal('(')
    add_terminal(')')
    add_terminal('=')

    add_rule('<program>', 'program <declaration part> <execution part> end')
    add_rule('<declaration part>', 'declaration <declaration list>')
    add_rule('<declaration list>', '<declaration>; <declaration list>')
    add_rule('<declaration list>', '<declaration>')
    add_rule('<declaration>', 'integer <variable list>')
    add_rule('<variable list>', 'i, <variable list>')
    add_rule('<variable list>', 'i')
    add_rule('<execution part>', 'execution <statement list>')
    add_rule('<statement list>', '<statement>; <statement list>')
    add_rule('<statement list>', '<statement>')
    add_rule('<statement>', 'i = <expression>')
    add_rule('<statement>', 'read(<input list>)')
    add_rule('<statement>', 'write(<output list>)')
    add_rule('<statement>', 'if <condition> then <statement>')
    add_rule('<statement>', 'if <condition> then <statement> else <statement>')
    add_rule(
        '<statement>', 'for i = <expression> through expression'
        'iterate <statement>')
    add_rule('<statement>', 'begin <statement list> end')
    add_rule('<input list>', 'i, <input list>')
    add_rule('<input list>', 'i')
    add_rule('<output list>', '<write member>, <output list>')
    add_rule('<write member>', '<expression>')
    add_rule('<write member>', 't')
    add_rule('<condition>', '<condition> r <condition>')
    add_rule('<condition>', '<condition> & <condition>')
    add_rule('<condition>', '<condition> | <condition>')
    add_rule('<condition>', '!<condition>')
    add_rule('<condition>', '(<condition>)')
    add_rule('<condition>', '<expression>')
    add_rule('<expression>', '<expression> + <term>')
    add_rule('<expression>', '<expression> - <term>')
    add_rule('<expression>', '<term>')
    add_rule('<term>', '<term> * <factor>')
    add_rule('<term>', '<term> / <factor>')
    add_rule('<term>', '<factor>')
    add_rule('<factor>', '(<expression>)')
    add_rule('<factor>', 'i')
    add_rule('<factor>', '#')

def add_nonterminal(char):
    Nonterminal.objects.get_or_create(char=char)[0]


def add_terminal(char):
    Terminal.objects.get_or_create(char=char)[0]


def add_rule(left_side, right_side):
    Rule.objects.get_or_create(left_side=left_side, right_side=right_side)[0]

if __name__ == '__main__':
    print('Starting Alan population script...')
    populate()
    print('Done')
