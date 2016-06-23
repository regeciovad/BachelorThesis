# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_ad_hoc.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.ad_hoc import ParserAdHoc
import time
from alan.models import Rule
from populate_alan import populate

class AdHocMethodTests(TestCase):

    def test_ad_hoc_empty_program(self):
        """
            Testing of empty code for parser.
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        exit_code = 0
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'] , '', '',
            ['<$, 0>', '<<statement_list>, 1>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, '', '', 1, '']
        output_expected = ['action[0, $] = f2', 'Byla použita Ad-hoc rutina číslo 2:',
                          'Na vstup byl vložen token [i, help]', 'action[0, i] = s9', 'action[9, $] = r16',
                          'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                          'action[7, $] = r14', 'pravidlo 14: <term> \u2192 <factor>',
                          'goto[0, <term>] = 6', 'action[6, $] = r11',
                          'pravidlo 11: <expression> \u2192 <term>', 'goto[0, <expression>] = 5',
                          'action[5, $] = r8', 'pravidlo 8: <condition> \u2192 <expression>',
                          'goto[0, <condition>] = 3', 'action[3, $] = r6',
                          'pravidlo 6: <statement> \u2192 <condition>', 'goto[0, <statement>] = 2',
                          'action[2, $] = r2', 'pravidlo 2: <statement_list> \u2192 <statement>',
                          'goto[0, <statement_list>] = 1', 'action[1, $] = acc', 'success']
        output, stack, state, exit = parser.parser_analysis([], grammar_list)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_empty_grammar_list(self):
        """
            Testing of empty list of grammar rules for parser.
            It should be error.
        """
        parser = ParserAdHoc()
        exit_code = 1
        lex_code = '[i, a]'
        output = (
            ['Chyba programu - prázdná množina pravidel'], [], [], exit_code)
        parser_result = parser.parser_analysis(lex_code)
        self.assertEqual(parser_result, output)

    def test_ad_hoc_a_semicolon(self):
        """
            Testing of code: a;, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]']
        exit_code = 0
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], '', '', ['<$, 0>', '<<statement_list>, 1>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, '', '', 1, '']
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
                           'action[11, $] = f1', 'Byla použita Ad-hoc rutina číslo 1:', 'Ze zásobníku byl vyňat token <;, 11>',
                           'action[2, $] = r2', 'pravidlo 2: <statement_list> \u2192 <statement>', 'goto[0, <statement_list>] = 1',
                           'action[1, $] = acc', 'success']
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_two_semicolons(self):
        """
            Testing of code: a;;b, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]', '[;]', '[i, b]']
        exit_code = 0
        stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<i, 9>'], '', '',
            ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<factor>, 7>'], '', '', ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<term>, 6>'],
            '', '', ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<expression>, 5>'], '', '', ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<condition>, 3>'],
            '', '', ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<statement>, 2>'], '', '', ['<$, 0>', '<<statement>, 2>', '<;, 11>', '<<statement_list>, 21>'],
            '', '', ['<$, 0>', '<<statement_list>, 1>'], '']
        state_expected = [0, 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, 9, '', '', 7, '', '', 6, '', '', 5, '', '',
                         3, '', '', 2, '', '', 21, '', '', 1, '']
        output_expected = ['action[0, i] = s9', 'action[9, ;] = r16', 'pravidlo 16: <factor> \u2192 i',
                          'goto[0, <factor>] = 7', 'action[7, ;] = r14', 'pravidlo 14: <term> \u2192 <factor>',
                          'goto[0, <term>] = 6', 'action[6, ;] = r11', 'pravidlo 11: <expression> \u2192 <term>',
                          'goto[0, <expression>] = 5', 'action[5, ;] = r8', 'pravidlo 8: <condition> \u2192 <expression>',
                          'goto[0, <condition>] = 3', 'action[3, ;] = r6', 'pravidlo 6: <statement> \u2192 <condition>',
                          'goto[0, <statement>] = 2', 'action[2, ;] = s11', 'action[11, ;] = f3', 'Byla použita Ad-hoc rutina číslo 3:',
                          'Ze vstupu byl odstraněn token [;]', 'action[11, i] = s9', 'action[9, $] = r16', 'pravidlo 16: <factor> \u2192 i',
                          'goto[11, <factor>] = 7', 'action[7, $] = r14', 'pravidlo 14: <term> \u2192 <factor>', 'goto[11, <term>] = 6',
                          'action[6, $] = r11', 'pravidlo 11: <expression> \u2192 <term>', 'goto[11, <expression>] = 5',
                          'action[5, $] = r8', 'pravidlo 8: <condition> \u2192 <expression>', 'goto[11, <condition>] = 3',
                          'action[3, $] = r6', 'pravidlo 6: <statement> \u2192 <condition>', 'goto[11, <statement>] = 2',
                          'action[2, $] = r2', 'pravidlo 2: <statement_list> \u2192 <statement>', 'goto[11, <statement_list>] = 21',
                          'action[21, $] = r1', 'pravidlo 1: <statement_list> \u2192 <statement> ; <statement_list>',
                          'goto[0, <statement_list>] = 1', 'action[1, $] = acc','success']
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    # In this point I realized how naive was my way of testing
    # This is actually (according to me) better way, much shorter and more independent on text of application
    # But I just could not delete all my work on these tests, so I will only change it in next test
    def test_ad_hoc_a_plus(self):
        """
            Testing of code: a +, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[16, $] = f2'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_a_b(self):
        """
            Testing of code: a b, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[9, i] = f3'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_two_plus(self):
        """
            Testing of code: a + + b, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]', '[+]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[16, +] = f3'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_a_less(self):
        """
            Testing of code: a <, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[r, <]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[12, $] = f2'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_bracket_without_end(self):
        """
            Testing of code: (a, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[20, $] = f4'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_bracket_two_in_end(self):
        """
            Testing of code: (a)), which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[)]', '[)]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[5, )] = f3'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_wrong_bracket(self):
        """
            Testing of code: )a;b, which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[)]', '[i, a]', '[;]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[0, )] = f3'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_empty_bracket(self):
        """
            Testing of code: (), which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[)]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[8, )] = f2'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_not_in_brackets(self):
        """
            Testing of code: (!a), which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[!]', '[i, a]', '[)]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[8, !] = f3'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_ad_hoc_bracket_and_op(self):
        """
            Testing of code: (a+b)c), which is a syntax error
        """
        parser = ParserAdHoc()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[+]', '[i, b]', '[)]', '[i, c]', '[)]']
        exit_code = 0
        output_expected = 'success'
        routine_expected = 'action[29, i] = f5'
        output, stack, state, exit = parser.parser_analysis(lex_code, grammar_list)
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        routine_expected = 'action[5, )] = f3'
        if not output_expected in output:
             raise TypeError("Ad-hoc did not fixed the error")
        if not routine_expected in output:
             raise TypeError("Ad-hoc did not use expected routine")
        self.assertEqual(exit, exit_code)
