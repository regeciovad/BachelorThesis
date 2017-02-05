# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_panic_mode_first.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.panic_mode_first import PanicModeParserFirst
from alan.models import Rule
from populate_alan import populate


class PanicModeFirstMethodTests(TestCase):

    def test_panic_mode_first_empty_program(self):
        """
            Testing of empty code for parser.
        """
        parser = PanicModeParserFirst()
        exit_code = 1
        output_expected = 'Syntaktická chyba - prázdný program'
        parser_result_expected = ['Panická metoda na tuto chybu nestačí.']
        output, [], [], exit, parser_result, [] = parser.parser_analysis()
        if not output_expected in output:
            raise TypeError("Something is wrong with checking empty program.")
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_empty_grammar_list(self):
        """
            Testing of empty list of grammar rules for parser.
            It should be error.
        """
        parser = PanicModeParserFirst()
        exit_code = 1
        lex_code = '[i, a]'
        output = (
            ['Chyba programu - prázdná množina pravidel'], [], [], exit_code, [], [])
        parser_result = parser.parser_analysis(lex_code)
        self.assertEqual(parser_result, output)

    def test_panic_mode_first_a_semicolon(self):
        """
            Testing of code: a;, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 'Na vstupu nebyl nalezen žádný symbol z této množiny.',
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], '', '']
        state_expected = [0, '', 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, ;] = r16',
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
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_two_semicolons(self):
        """
            Testing of code: a;;b, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[;]', '[;]', '[i, b]']
        exit_code = 0
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[;]', '[i, b]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 'Nalezen symbol: [i, b]',
                                 "Hledáme v zásobníku synchronizační neterminál: ",
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 'Zásobník vyprázdněn do neterminálu: <<statement>, 2>',
                                 "Dále hledáme na vstupu symbol z Follow(<statement>):",
                                 "['$', ';', 'r', '&', '|']",
                                 "Nalezen symbol: [$]",
                                 'Aktualizace stavu: 2',
                                 'Ukončení Panického módu.', '']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<;, 11>'], '', '', ['<$, 0>', '<<statement>, 2>'], '', '',
            ['<$, 0>', '<<statement_list>, 1>'], '', '']
        state_expected = [0, '', 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 11, '', '', 2, '', '', 1, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, ;] = r16',
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
                           'action[11, ;] = ', 'syntaktická chyba', 'action[2, $] = r2',
                           'pravidlo 2: <statement_list> \u2192 <statement>',
                           'goto[0, <statement_list>] = 1', 'action[1, $] = acc', 'success']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_a_plus(self):
        """
            Testing of code: a +, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Na vstupu nebyl nalezen žádný symbol z této množiny.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'],
            ['<$, 0>', '<<expression>, 5>', '<+, 16>'], '', '']
        state_expected = [0, '', 9, '', '', 7, '', '', 6, '', '', 5, 16, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, +] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, +] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, +] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, +] = s16',
                           'action[16, $] = ', 'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_a_b(self):
        """
            Testing of code: a b, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[i, b]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[i, b]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 'Nalezen symbol: [i, b]',
                                 'Hledáme v zásobníku synchronizační neterminál: ',
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 'Nebyl nalezen synchronizační neterminál.',
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '']
        state_expected = [0, '', 9, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, i] = ',
                          'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_two_plus(self):
        """
            Testing of code: a + + b, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[+]', '[+]', '[i, b]']
        exit_code = 0
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[+]', '[i, b]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Nalezen symbol: [i, b]",
                                 'Hledáme v zásobníku synchronizační neterminál: ',
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 'Zásobník vyprázdněn do neterminálu: <<expression>, 5>',
                                 'Dále hledáme na vstupu symbol z Follow(<expression>):',
                                 "['$', ';', 'r', '&', '|', '+', '-', ')']",
                                 "Nalezen symbol: [$]",
                                 'Aktualizace stavu: 5',
                                 'Ukončení Panického módu.', '']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'],
            ['<$, 0>', '<<expression>, 5>', '<+, 16>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'], '', '',
            ['<$, 0>', '<<statement_list>, 1>'], '', '']
        state_expected = [0, '', 9, '', '', 7, '', '', 6, '', '', 5, 16, '', '', 5, '', '', 3, '', '', 2, '', '', 1, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, +] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[0, <factor>] = 7',
                           'action[7, +] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[0, <term>] = 6', 'action[6, +] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[0, <expression>] = 5', 'action[5, +] = s16',
                           'action[16, +] = ', 'syntaktická chyba','action[5, $] = r8',
                           'pravidlo 8: <condition> \u2192 <expression>',
                           'goto[0, <condition>] = 3', 'action[3, $] = r6',
                           'pravidlo 6: <statement> \u2192 <condition>',
                           'goto[0, <statement>] = 2', 'action[2, $] = r2',
                           'pravidlo 2: <statement_list> \u2192 <statement>', 'goto[0, <statement_list>] = 1',
                           'action[1, $] = acc', 'success']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_a_less(self):
        """
            Testing of code: a <, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[i, a]', '[r, <]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Na vstupu nebyl nalezen žádný symbol z této množiny.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<i, 9>'], '', '', ['<$, 0>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'],
            ['<$, 0>', '<<statement>, 2>', '<r, 12>'], '', '']
        state_expected = [0, '', 9, '', '', 7, '', '', 6, '', '', 5, '', '', 3, '', '', 2, 12, '', '']
        output_expected = ['Read the first token', 'action[0, i] = s9', 'action[9, r] = r16',
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
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_bracket_without_end(self):
        """
            Testing of code: (a, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Na vstupu nebyl nalezen žádný symbol z této množiny.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], '', '']
        state_expected = [0, '', 8, 9, '', '', 7, '', '', 6, '', '', 20, '', '']
        output_expected = ['Read the first token', 'action[0, (] = s8', 'action[8, i] = s9', 'action[9, $] = r16',
                           'pravidlo 16: <factor> \u2192 i', 'goto[8, <factor>] = 7',
                           'action[7, $] = r14',
                           'pravidlo 14: <term> \u2192 <factor>',
                           'goto[8, <term>] = 6', 'action[6, $] = r11',
                           'pravidlo 11: <expression> \u2192 <term>',
                           'goto[8, <expression>] = 20', 'action[20, $] = ',
                           'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_bracket_two_in_end(self):
        """
            Testing of code: (a)), which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[)]', '[)]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[)]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Na vstupu nebyl nalezen žádný symbol z této množiny.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<), 29>'], '', '',
            ['<$, 0>', '<<factor>, 7>'], '', '', ['<$, 0>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<<expression>, 5>'], '', '']
        state_expected = [0, '', 8, 9, '', '', 7, '', '', 6, '', '', 20, 29, '', '', 7, '', '', 6, '', '', 5, '', '']
        output_expected = ['Read the first token', 'action[0, (] = s8', 'action[8, i] = s9', 'action[9, )] = r16',
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
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_wrong_bracket(self):
        """
            Testing of code: )a;b, which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[)]', '[i, a]', '[;]', '[i, b]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[)]', '[i, a]', '[;]', '[i, b]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 'Nalezen symbol: [i, a]',
                                 'Hledáme v zásobníku synchronizační neterminál: ',
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 "Nebyl nalezen synchronizační neterminál.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', '', '']
        state_expected = [0, '', '', '']
        output_expected = ['Read the first token', 'action[0, )] = ', 'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_empty_bracket(self):
        """
            Testing of code: (), which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[)]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[)]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Na vstupu nebyl nalezen žádný symbol z této množiny.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<(, 8>'], '', '']
        state_expected = [0, '', 8, '', '']
        output_expected = ['Read the first token', 'action[0, (] = s8', 'action[8, )] = ', 'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_not_in_brackets(self):
        """
            Testing of code: (!a), which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[!]', '[i, a]', '[)]']
        exit_code = 1
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[!]', '[i, a]', '[)]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Nalezen symbol: [!]",
                                 "Hledáme v zásobníku synchronizační neterminál: ",
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 "Nebyl nalezen synchronizační neterminál.",
                                 'Panická metoda na tuto chybu nestačí.']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<(, 8>'], '', '']
        state_expected = [0, '', 8, '', '']
        output_expected = ['Read the first token', 'action[0, (] = s8', 'action[8, !] = ', 'syntaktická chyba']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)

    def test_panic_mode_first_bracket_and_op(self):
        """
            Testing of code: (a+b)c), which is a syntax error
        """
        parser = PanicModeParserFirst()
        populate()
        grammar = Rule.objects.order_by('id')
        grammar_list = []
        grammar_list.append({'id': 0, 'left': '', 'right': ''})
        for g in grammar:
            grammar_list.append({'id': g.id, 'left': g.left_hand_side, 'right': g.right_hand_side})
        lex_code = ['[(]', '[i, a]', '[+]', '[i, b]', '[)]', '[i, c]', '[)]']
        exit_code = 0
        parser_result_expected = ['Zahájení Panického módu s množinou First.',
                                 "Aktuální vstup: ['[i, c]', '[)]', '[$]']",
                                 "Hledáme symbol z množiny First: ['!', '(', 'i', '#']",
                                 "Nalezen symbol: [i, c]",
                                 "Hledáme v zásobníku synchronizační neterminál: ",
                                 "['<condition>', '<statement>', '<statement_list>', '<expression>']",
                                 "Zásobník vyprázdněn do neterminálu: <<expression>, 20>",
                                 "Dále hledáme na vstupu symbol z Follow(<expression>):",
                                 "['$', ';', 'r', '&', '|', '+', '-', ')']",
                                 "Nalezen symbol: [)]",
                                 "Aktualizace stavu: 20",
                                 "Ukončení Panického módu.", '']
        stack_expected = [['<$, 0>'], '', ['<$, 0>', '<(, 8>'], ['<$, 0>', '<(, 8>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<term>, 6>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>'],
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<i, 9>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<<factor>, 7>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<+, 16>', '<<term>, 25>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<), 29>'], '', '',
            ['<$, 0>', '<(, 8>', '<<expression>, 20>'], ['<$, 0>', '<(, 8>', '<<expression>, 20>', '<), 29>'], '', '',
            ['<$, 0>', '<<factor>, 7>'], '', '', ['<$, 0>', '<<term>, 6>'], '', '', ['<$, 0>', '<<expression>, 5>'], '', '',
            ['<$, 0>', '<<condition>, 3>'], '', '', ['<$, 0>', '<<statement>, 2>'], '', '', ['<$, 0>', '<<statement_list>, 1>'], '', '']
        state_expected = [0, '', 8, 9, '', '', 7, '', '', 6, '', '', 20, 16, 9, '', '', 7, '', '', 25, '', '', 20, 29, '', '', 20, 29, '', '', 7,
                         '', '', 6, '', '', 5, '', '', 3, '', '', 2, '', '', 1, '', '']
        output_expected = ['Read the first token', 'action[0, (] = s8', 'action[8, i] = s9', 'action[9, +] = r16',
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
                           'syntaktická chyba', 'action[20, )] = s29', 'action[29, $] = r15',
                           'pravidlo 15: <factor> \u2192 ( <expression> )',
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
                           'goto[0, <statement_list>] = 1', 'action[1, $] = acc', 'success']
        output, stack, state, exit, parser_result, lex_input = parser.parser_analysis(lex_code, grammar_list)
        self.assertEqual(parser_result, parser_result_expected)
        self.assertEqual(output, output_expected)
        self.assertEqual(stack, stack_expected)
        self.assertEqual(state, state_expected)
        self.assertEqual(exit, exit_code)
