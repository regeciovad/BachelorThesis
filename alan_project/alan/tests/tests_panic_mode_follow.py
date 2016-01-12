# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_panic_mode_follow.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.panic_mode import PanicModeParser
import time


class PanicModeFollowMethodTests(TestCase):

    def test_panic_mode_empty_program(self):
        """
            Testing of empty code for parser.
        """
        parser = PanicModeParser()
        exit_code = 1
        output = 'Syntaktická chyba - prázdný program'
        parser_result = ['Panická metoda na tuto chybu nestačí.']
        output_expected, [], [], exit, parser_result_expected = parser.parser_analysis()
        if not output in output_expected:
            raise TypeError("Something is wrong with checking empty program.")
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(exit, exit_code)

    def test_parser_empty_grammar_list(self):
        """
            Testing of empty list of grammar rules for parser.
            It should be error.
        """
        parser = PanicModeParser()
        exit_code = 1
        lex_code = '[i, a]'
        output = (
            ['Chyba programu - prázdná množina pravidel'], [], [], exit_code, [])
        parser_result = parser.parser_analysis(lex_code)
        self.assertEqual(parser_result, output)
