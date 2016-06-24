# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_parser.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.parser import Parser
from alan.models import Rule
from populate_alan import populate


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
                           'pravidlo 16: <factor> \u2192 i',
                           'goto[0, <factor>] = 7', 'action[7, $] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, $] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, $] = r8',
                           'pravidlo 8: <condition> \u2192 <expression>',
                           'goto[0, <condition>] = 3', 'action[3, $] = r6',
                           'pravidlo 6: <statement> \u2192 <condition>',
                           'goto[0, <statement>] = 2', 'action[2, $] = r2',
                           'pravidlo 2: <statement_list> \u2192 <statement>',
                           'goto[0, <statement_list>] = 1',
                           'action[1, $] = acc', 'success']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_a_semicolon(self):
        """
            Testing of code: a;, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, '']
        output_expected = ['action[0, i] = s9', 'action[9, ;] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, ;] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, ;] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, ;] = r8',
                           'pravidlo 8: <condition> \u2192 <expression>',
                           'goto[0, <condition>] = 3', 'action[3, ;] = r6',
                           'pravidlo 6: <statement> \u2192 <condition>',
                           'goto[0, <statement>] = 2', 'action[2, ;] = s11',
                           'action[11, $] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_two_semicolons(self):
        """
            Testing of code: a;;b, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]', '[;]', '[i, b]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, '']
        output_expected = ['action[0, i] = s9', 'action[9, ;] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, ;] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, ;] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, ;] = r8',
                           'pravidlo 8: <condition> \u2192 <expression>',
                           'goto[0, <condition>] = 3', 'action[3, ;] = r6',
                           'pravidlo 6: <statement> \u2192 <condition>',
                           'goto[0, <statement>] = 2', 'action[2, ;] = s11',
                           'action[11, ;] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_a_plus(self):
        """
            Testing of code: a +, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'],
            ['<$, 0>', '<<expression>, 5>', '<+, 16>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, 16, '']
        output_expected = ['action[0, i] = s9', 'action[9, +] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, +] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, +] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, +] = s16',
                           'action[16, $] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_a_b(self):
        """
            Testing of code: a b, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[i, b]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '']
        state_expected = [0, 9, '']
        output_expected = ['action[0, i] = s9', 'action[9, i] = ',
                          'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_two_plus(self):
        """
            Testing of code: a + + b, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]', '[+]', '[i, b]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'],
            ['<$, 0>', '<<expression>, 5>', '<+, 16>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, 16, '']
        output_expected = ['action[0, i] = s9', 'action[9, +] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, +] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, +] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, +] = s16',
                           'action[16, +] = ', 'syntaktická chyba']
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
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, r] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, r] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, r] = r8',
                           'pravidlo 8: <condition> \u2192 <expression>',
                           'goto[0, <condition>] = 3', 'action[3, r] = r6',
                           'pravidlo 6: <statement> \u2192 <condition>',
                           'goto[0, <statement>] = 2', 'action[2, r] = s12',
                           'action[12, $] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_bracket_without_end(self):
        """
            Testing of code: (a, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], '']
        state_expected = [0, 8, 9, '', '', 7, '', '', 6, '', '', 20, '']
        output_expected = ['action[0, (] = s8', 'action[8, i] = s9', 'action[9, $] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[8, <factor>] = 7',
                           'action[7, $] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[8, <term>] = 6', 'action[6, $] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[8, <expression>] = 20', 'action[20, $] = ',
                           'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_bracket_two_in_end(self):
        """
            Testing of code: (a)), which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[)]', '[)]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<), 29>'], '', '',
            ['<$, 0>', '<<factor>, 7>'], '', '', ['<$, 0>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<<expression>, 5>'], '']
        state_expected = [0, 8, 9, '', '', 7, '', '', 6, '', '', 20, 29, '', '', 7, '', '', 6, '', '', 5, '']
        output_expected = ['action[0, (] = s8', 'action[8, i] = s9', 'action[9, )] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[8, <factor>] = 7',
                           'action[7, )] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[8, <term>] = 6', 'action[6, )] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[8, <expression>] = 20', 'action[20, )] = s29', 'action[29, )] = r15',
                           'pravidlo 15: <factor> \u2192 ( <expression> )',
                           'goto[0, <factor>] = 7', 'action[7, )] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, )] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, )] = ',
                           'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_wrong_bracket(self):
        """
            Testing of code: )a;b, which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[)]', '[i, a]', '[;]', '[i, b]']
        exit_code = 1
        stack_expected = [['<$, 0>'], '']
        state_expected = [0, '']
        output_expected = ['action[0, )] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_empty_bracket(self):
        """
            Testing of code: (), which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[)]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<(, 8>'], '']
        state_expected = [0, 8, '']
        output_expected = ['action[0, (] = s8', 'action[8, )] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_not_in_brackets(self):
        """
            Testing of code: (!a), which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[!]', '[i, a]', '[)]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<(, 8>'], '']
        state_expected = [0, 8, '']
        output_expected = ['action[0, (] = s8', 'action[8, !] = ', 'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_bracket_and_op(self):
        """
            Testing of code: (a+b)c), which is a syntax error
        """
        parser = Parser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[+]', '[i, b]', '[)]', '[i, c]', '[)]']
        exit_code = 1
        stack_expected = [['<$, 0>'], ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>'],
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<<term>, 25>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<), 29>'], '']
        state_expected = [0, 8, 9, '', '', 7, '', '', 6, '', '', 20, 16, 9, '', '', 7, '', '', 25, '', '', 20, 29, '']
        output_expected = ['action[0, (] = s8', 'action[8, i] = s9', 'action[9, +] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[8, <factor>] = 7',
                           'action[7, +] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[8, <term>] = 6', 'action[6, +] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[8, <expression>] = 20', 'action[20, +] = s16', 'action[16, i] = s9', 'action[9, )] = r16',
                           'pravidlo 16: <factor> \u2192 i',
                           'goto[16, <factor>] = 7', 'action[7, )] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[16, <term>] = 25', 'action[25, )] = r9',
                           'pravidlo 9: <expression> \u2192 <expression> + <term>',
                           'goto[8, <expression>] = 20', 'action[20, )] = s29', 'action[29, i] = ',
                           'syntaktická chyba']
        parser_result, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)
