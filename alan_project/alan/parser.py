# Advanced Error Recovery during Bottom-Up Parsing
# File: parser.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from .stack import Stack
from .lrtable import LRTable


class Parser(object):

    def __init__(self):
        # Output of syntax analysis
        self.result = []
        # Exit code: 0 == ok, 1 == error
        self.exit_code = 0
        # Stack and it's records
        self.stack = Stack()
        self.stackHistory = []
        # State records
        self.stateHistory = []
        # LR Table
        self.lrtable = LRTable()

    def parser_analysis(self, tokens=[], grammar=[]):
        """ Basic syntax analysis
            Input: list of tokens, grammar rules
            Output: result of syntax analysis, stack history, state history
                    and exit code"""

        # List of tokens are missing
        if tokens == []:
            self.result.append('Syntaktická chyba - prázdný program')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code)

        # List of grammar rules are missing
        if grammar == []:
            self.result.append('Chyba programu - prázdná množina pravidel')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code)

        # Adding end
        if tokens[-1:] != '[$]':
            tokens.append('[$]')
        # Get LR Table
        action, goto = self.lrtable.generate_table()
        # Push end-token into stack
        self.stack.push('<$, 0>')
        self.stackHistory = [self.stack.get_stack()]
        # Set state
        state = 0
        self.stateHistory = [state]
        # Get first tokens
        token_number = 0
        token = tokens[token_number]
        token_number += 1

        # Main loop
        while (True):
            # Look into action part of table - action[state][token]
            a = token[1]
            cell = action[state][a]
            self.result.append(
                'action[' + str(state) + ', ' + a + '] = ' + cell)

            # action[state][token] == s(q), q is a number
            # Shift (read) new token and change state
            if cell.startswith('s'):
                q = cell[1:]
                self.stack.push('<' + a + ', ' + q + '>')
                self.stackHistory.append(self.stack.get_stack())
                try:
                    token = tokens[token_number]
                    token_number += 1
                except IndexError:
                    self.result.append('syntaktická chyba')
                    self.exit_code = 1
                    break
                a = token[1]
                state = int(q)
                self.stateHistory.append(state)

            # action[state][token] == r(p), p is a number of rule
            # Apply rule, change stack and state
            elif cell.startswith('r'):
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
                    actual_state = int(
                        self.stack.get_topmost().split(',')[1][:-1])
                    if actual_state == '':
                        self.result.append(
                            'Chyba: analýza se dostala do nedefinovaného stavu')
                        self.exit_code = 1
                        break
                    state = int(goto[actual_state][left])
                    self.result.append('goto[' + str(actual_state) + ', ' + left + '] = ' + str(state))
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.stateHistory.append(state)
                    self.stack.push(('<' + left + ', ' + str(state) + '>'))
                    self.stackHistory.append(self.stack.get_stack())
                else:
                    self.result.append(
                        'Chyba: analýza se dostala do nedefinovaného stavu')
                    self.exit_code = 1
                    break

            # action[state][token] == acc, source code is correct
            elif cell.startswith('acc'):
                self.result.append('success')
                self.stackHistory.append('')
                self.stateHistory.append('')
                break

            # action[state][token] == blank, source code has some syntax error
            else:
                self.result.append('syntaktická chyba')
                self.exit_code = 1
                self.stackHistory.append('')
                self.stateHistory.append('')
                break

        # Return results
        return (self.result, self.stackHistory, self.stateHistory,
                self.exit_code)
