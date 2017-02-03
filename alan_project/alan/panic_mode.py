# Advanced Error Recovery during Bottom-Up Parsing
# File: panic_mode.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from .stack import Stack
from .lrtable import LRTable


class PanicModeParser(object):

    def __init__(self):
        # Output of syntax analysis
        self.result = []
        # Output of recovery method Panic Mode
        self.panic_mode_result = []
        # Exit code: 0 == ok, 1 == error
        self.exit_code = 0
        # Stack and its records
        self.stack = Stack()
        self.stackHistory = []
        # State records
        self.stateHistory = []
        # Input lexems
        self.lex_input = []
        # LR Table
        self.lrtable = LRTable()
        self.panic_time = 0

    def parser_analysis(self, tokens=[], grammar=[]):
        """ Advanced syntax analysis with Panic Mode recovery
            Input: list of tokens, grammar rules
            Output: result of syntax analysis, stack history, state history,
            panic mode recovery records and exit code"""

        self.tokens = tokens
        # List of tokens are missing
        if self.tokens == []:
            self.panic_mode_result.append("Panická metoda na tuto chybu nestačí.")
            self.result.append('Syntaktická chyba - prázdný program')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code, self.panic_mode_result, self.lex_input)

        # List of grammar rules are missing
        if grammar == []:
            self.result.append('Chyba programu - prázdná množina pravidel')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code, self.panic_mode_result, self.lex_input)

        # Adding end
        if self.tokens[-1:] != '[$]':
            self.tokens.append('[$]')
        # Get LR Table
        self.action, self.goto = self.lrtable.generate_table()
        # Push end-token into stack
        self.stack.push('<$, 0>')
        self.stackHistory = [self.stack.get_stack()]
        # Set state
        self.state = 0
        self.stateHistory = [self.state]
        # Get first tokens
        self.token_number = 0
        self.token = self.tokens[self.token_number]
        self.token_number += 1
        self.stackHistory.append('')
        self.stateHistory.append('')
        self.result.append('Read the first token: ')
        self.lex_input.append('<strong style="color:orange">' + ''.join(self.token) + '</strong>' + ''.join(self.tokens[self.token_number:]))

        # Main loop
        while True:
            # Look into action part of table - action[state][token]
            a = self.token[1]
            cell = self.action[self.state][a]
            self.result.append(
                'action[' + str(self.state) + ', ' + a + '] = ' + cell)

            # action[state][token] == s(q), q is a number
            # Shift (read) new token and change state
            if cell.startswith('s'):
                q = cell[1:]
                self.stack.push('<' + a + ', ' + q + '>')
                self.stackHistory.append(self.stack.get_stack())
                try:
                    self.token = self.tokens[self.token_number]
                    self.token_number += 1
                    self.lex_input.append('<strong style="color:orange">' + ''.join(self.token) + '</strong>' + ''.join(self.tokens[self.token_number:]))
                except IndexError:
                    self.result.append('syntaktická chyba')
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.lex_input.append('')
                    break
                a = self.token[1]
                self.state = int(q)
                self.stateHistory.append(self.state)

            # action[state][token] == r(p), p is a number of rule
            # Apply rule, change stack and state
            elif cell.startswith('r'):
                self.lex_input.append('')
                p = cell[1:]
                left = grammar[int(p)]['left']
                right = grammar[int(p)]['right']
                handle = right.split(' ')
                pop_stack = []
                for x in range(len(handle)):
                    pop_stack.append(self.stack.pop().split(',')[0][1:])
                pop_stack.reverse()
                if str(handle) == str(pop_stack):
                    self.result.append(
                        'pravidlo ' + p + ': ' + left + ' \u2192 ' + right)
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.lex_input.append('')
                    actual_state = int(
                        self.stack.get_topmost().split(',')[1][:-1])
                    if actual_state == '':
                        self.result.append('gotochyba')
                        self.exit_code = 1
                        break
                    self.state = int(self.goto[actual_state][left])
                    self.result.append('goto[' + str(actual_state) + ', ' + left + '] = ' + str(self.state))
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.lex_input.append('')
                    self.stateHistory.append(self.state)
                    self.stack.push('<' + left + ', ' + str(self.state) + '>')
                    self.stackHistory.append(self.stack.get_stack())
                else:
                    self.result.append('syntaktická chyba')
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.lex_input.append('')
                    self.exit_code = 1
                    break

            # action[state][token] == acc, source code is correct
            elif cell.startswith('acc'):
                self.stackHistory.append('')
                self.stateHistory.append('')
                self.lex_input.append('')
                self.result.append('success')
                self.exit_code = 0
                self.stackHistory.append('')
                self.stateHistory.append('')
                self.lex_input.append('')
                break

            # action[state][token] == blank, source code has some syntax error
            else:
                self.stackHistory.append('')
                self.stateHistory.append('')
                self.lex_input.append('')
                self.result.append('syntaktická chyba')
                self.exit_code = 1
                self.stackHistory.append('')
                self.stateHistory.append('')
                self.lex_input.append('')
                panic_mode_exit = self.panic_mode()
                self.stackHistory.append(self.stack.get_stack())
                self.lex_input.append('<strong style="color:orange">' + ''.join(self.token) + '</strong>' + ''.join(self.tokens[self.token_number:]))
                if panic_mode_exit == 1:
                    break

        # Return results
        return (self.result, self.stackHistory, self.stateHistory,
                self.exit_code, self.panic_mode_result, self.lex_input)

    def panic_mode(self):
        """ Panic Mode recovery
            This method is looking for the shortest substring in input.
            Panic mode skips it and continues in parsing.
            This classic version is using synchronization tokens
            with their sets Follow(). """

        self.panic_mode_result.append("Zahájení Panického módu.")
        synchronization_tokens = ['<term>', '<expression>', '<condition>',
                                  '<statement>', '<statement_list>']

        while True:
            popped = self.stack.pop()
            if str(popped) == '<$, 0>' or popped is None:
                self.panic_mode_result.append("Zásobník byl plně vyprázdněn.")
                self.panic_mode_result.append("Panická metoda na tuto chybu nestačí.")
                return 1
            popped_token = popped.split(',')[0][1:]
            if popped_token in synchronization_tokens:
                break

        self.panic_mode_result.append("Zásobník vyprázdněn až po: " + str(self.stack.get_stack()))
        self.panic_mode_result.append("Nalezen neterminál: " + popped_token)

        if popped_token == '<term>':
            follow = ['$', ';', 'r', '&', '|', '+', '-', ')']
            next = '<expression>'
        elif popped_token == '<expression>':
            follow = ['$', ';', 'r', '&', '|']
            next = '<condition>'
        elif popped_token == '<condition>':
            follow = ['$', ';', 'r', '&', '|']
            next = '<statement>'
        elif popped_token == '<statement>':
            follow = ['$']
            next = '<statement_list>'
        elif popped_token == '<statement_list>':
            follow = ['$']
            next = '<statement_list>'

        self.panic_mode_result.append("Aktuální vstup: " + str(self.tokens[self.token_number-1:]))
        self.panic_mode_result.append("Hledáme symbol z množiny Follow(" + next + "): " + str(follow))

        while True:
            if self.token[1] in follow:
                break
            else:
                try:
                    self.token = self.tokens[self.token_number]
                    self.token_number += 1
                except IndexError:
                    self.panic_mode_result.append("Nebyl nalezen token z množiny Follow.")
                    self.panic_mode_result.append("Panická metoda na tuto chybu nestačí.")
                    return 1
        self.panic_mode_result.append("Nalezen symbol: " + str(self.token))
        state = int(self.stack.get_topmost().split(',')[1][:-1])
        goto_state = self.goto[state][next]
        if goto_state == '':
            self.panic_mode_result.append("Parser se dostal do nedefinovaného stavu.")
            self.panic_mode_result.append("Panická metoda na tuto chybu nestačí.")
            return 1
        self.state = int(self.goto[state][next])
        self.panic_mode_result.append(
            'goto[' + str(state) + ', ' + str(next) + '] = ' + str(self.state))
        self.stack.push('<' + str(next) + ', ' + str(self.state) + '>')
        self.panic_mode_result.append(
            'Vloženo na zásobník: ' + '<' + str(next) + ', ' +
            str(self.state) + '>')
        self.panic_mode_result.append('Ukončení Panického módu.')
        self.panic_mode_result.append('')
        return 0
