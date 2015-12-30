# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_panic_mode_follow.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from .panic_mode import PanicModeParser
import time

class PanicModeFollowMethodTests(TestCase):

    def test_scanner_empty_program(self):
        """
            Test of empty program
        """
        pass
        """parser = PanicModeParser()
        tokens = []
        grammar_list = get_grammar()
        begin = time.clock()
        parser_result, stack, state, exit_code, panic_mode = parser.parser_analysis(tokens, grammar_list)
        end = time.clock()
        mytime = end - begin
        parser_result.append("Čas zotavení: %f \u03BCs" % mytime)"""

