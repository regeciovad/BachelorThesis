# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_parser.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.parser import Parser
from alan.models import Rule
from populate_alan_newbie import populate


class ParserMethodTests(TestCase):

    def test_parser_empty_code(self):
        """
            Testing of empty code for parser. It should be error.
        """
        parser = Parser()
        exit_code = 1
        output = (['Syntaktická chyba - prázdný program'], [], [], exit_code)
        parser_result = parser.parser_analysis()
        self.assertEqual(parser_result, output)

    def test_parser_empty_grammar_list(self):
        """
            Testing of empty list of grammar rules for parser.
            It should be error.
        """
        parser = Parser()
        exit_code = 1
        lex_code = '[i, a]'
        output = (
            ['Chyba programu - prázdná množina pravidel'], [], [], exit_code)
        parser_result = parser.parser_analysis(lex_code)
        self.assertEqual(parser_result, output)

    def test_parser_a(self):
        """
            Testing of code: a
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]']
        exit_code = 0
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'], '', '',
            ['<$, 0>', '<<statement_list>, 1>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, '', '', 1, '']
        output_expected = ['action[0, i] = s9', 'action[9, $] = r16',
                           'pravidlo 16: <factor> -> i',
                           'goto[0, <factor>] = 7', 'action[7, $] = r14',
                           'pravidlo 14: <term> -> <factor>',
                           'goto[0, <term>] = 6', 'action[6, $] = r11',
                           'pravidlo 11: <expression> -> <term>',
                           'goto[0, <expression>] = 5', 'action[5, $] = r8',
                           'pravidlo 8: <condition> -> <expression>',
                           'goto[0, <condition>] = 3', 'action[3, $] = r6',
                           'pravidlo 6: <statement> -> <condition>',
                           'goto[0, <statement>] = 2', 'action[2, $] = r2',
                           'pravidlo 2: <statement_list> -> <statement>',
                           'goto[0, <statement_list>] = 1',
                           'action[1, $] = acc', 'success']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_a_less(self):
        """
            Testing of code: a <, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[r, <]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<r, 12>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 12, '']
        output_expected = ['action[0, i] = s9', 'action[9, r] = r16',
                           'pravidlo 16: <factor> -> i', 'goto[0, <factor>] = 7',
                           'action[7, r] = r14',
                           'pravidlo 14: <term> -> <factor>',
                           'goto[0, <term>] = 6', 'action[6, r] = r11',
                           'pravidlo 11: <expression> -> <term>',
                           'goto[0, <expression>] = 5', 'action[5, r] = r8',
                           'pravidlo 8: <condition> -> <expression>',
                           'goto[0, <condition>] = 3', 'action[3, r] = r6',
                           'pravidlo 6: <statement> -> <condition>',
                           'goto[0, <statement>] = 2', 'action[2, r] = s12',
                           'action[12, $] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)
