# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_alan_method.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.alan_method import AlanMethodParser
from alan.models import Rule
from populate_alan import populate


class AlanMethodTests(TestCase):

    def test_alan_method_empty_program(self):
        """
            Testing of empty code for parser.
        """
        parser = AlanMethodParser()
        exit_code = 1
        output_expected = 'Syntaktická chyba - prázdný program'
        parser_result_expected = []
        output, [], [], exit, parser_result = parser.parser_analysis()
        if output_expected not in output:
            raise TypeError("Something is wrong with checking empty program.")
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(exit, exit_code)

    def test_alan_method_empty_grammar_list(self):
        """
            Testing of empty list of grammar rules for parser.
            It should be error.
        """
        parser = AlanMethodParser()
        exit_code = 1
        lex_code = '[i, a]'
        output = (
            ['Chyba programu - prázdná množina pravidel'], [], [], exit_code, [])
        parser_result = parser.parser_analysis(lex_code)
        self.assertEqual(parser_result, output)

    def test_alan_method_a_semicolon(self):
        """
            Testing of code: a;, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<statement_list> \u2192 <statement> ; <statement_list>'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_two_semicolons(self):
        """
            Testing of code: a;;b, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]', '[;]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<statement_list> \u2192 <statement> ; <statement_list>'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_a_plus(self):
        """
            Testing of code: a +, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<expression> \u2192 <expression> + <term>'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_a_b(self):
        """
            Testing of code: a b, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<factor> \u2192 i'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_two_plus(self):
        """
            Testing of code: a + + b, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]', '[+]', '[i, b]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<expression> \u2192 <expression> + <term>'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_a_less(self):
        """
            Testing of code: a <, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[r, <]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<statement> \u2192 <statement> r <condition>'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_bracket_without_end(self):
        """
            Testing of code: (a, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]']
        exit_code = 0
        output_expected = 'success'
        rule_expected = '<factor> \u2192 ( <expression> )'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected not in output:
            raise TypeError("Alan method did not fixed the error")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_bracket_two_in_end(self):
        """
            Testing of code: (a)), which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[)]', '[)]']
        exit_code = 1
        output_expected = 'success'
        rule_expected = '<factor> \u2192 ( <expression> )'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected in output:
            raise TypeError("Really?")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_wrong_bracket(self):
        """
            Testing of code: )a;b, which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[)]', '[i, a]', '[;]', '[i, b]']
        exit_code = 1
        output_expected = 'success'
        rule_expected = 'Nenalazen žádný záchytný token.'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected in output:
            raise TypeError("Really?")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_empty_bracket(self):
        """
            Testing of code: (), which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[)]']
        exit_code = 1
        output_expected = 'success'
        rule_expected = '<factor> \u2192 ( <expression> )'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected in output:
            raise TypeError("Really?")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_not_in_brackets(self):
        """
            Testing of code: (!a), which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[!]', '[i, a]', '[)]']
        exit_code = 1
        output_expected = 'success'
        rule_expected = '<factor> \u2192 ( <expression> )'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected in output:
            raise TypeError("Really?")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)

    def test_alan_method_bracket_and_op(self):
        """
            Testing of code: (a+b)c), which is a syntax error
        """
        parser = AlanMethodParser()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[+]', '[i, b]', '[)]', '[i, c]', '[)]']
        exit_code = 1
        output_expected = 'success'
        rule_expected = '<factor> \u2192 ( <expression> )'
        output, stack, state, exit, parser_result = parser.parser_analysis(lex_code, grammar_list)
        if output_expected in output:
            raise TypeError("Really?")
        if rule_expected not in parser_result:
            raise TypeError("Alan method  did not use expected routine")
        self.assertEqual(exit, exit_code)
