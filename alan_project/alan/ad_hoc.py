# Advanced Error Recovery during Bottom-Up Parsing
# File: ad_hoc.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from .stack import Stack
from .lrtable import LRTable
import time


class ParserAdHoc(object):

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
        action, goto = self.lrtable.genereate_ad_hoc_action()
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
                        self.result.append('gotochyba')
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
                    self.result.append('syntaktická chyba')
                    self.exit_code = 1
                    break

            # action[state][token] == acc, source code is correct
            elif cell.startswith('acc'):
                self.result.append('success')
                self.stackHistory.append('')
                self.stateHistory.append('')
                break

            elif cell.startswith('f'):
                function = cell[1:]
                if function == '1':
                    """ Diagnostic no. 1: Pop stack
                        Pops up one terminal from stack and returns actual state
                        from top of the stack.
                        Example: a; """
                    popped = self.stack.pop()
                    state = int(self.stack.get_topmost().split(',')[1][:-1])
                    self.result.append('Byla použita Ad-hoc rutina číslo 1:')
                    self.result.append('Ze zásobníku byl vyňat token '
                        + popped)

                elif function == '2':
                    """ Diagnostic no. 2: Add variable
                        Adds token [i, help] into input.
                        Example: a+ """
                    token = '[i, help]'
                    token_number -= 1
                    self.result.append('Byla použita Ad-hoc rutina číslo 2:')
                    self.result.append('Na vstup byl vložen token [i, help]')

                elif function == '3':
                    """ Diagnostic no. 3: Remove token
                        Removes token from input.
                        Example: (a)) """
                    removed = token
                    token = tokens[token_number]
                    token_number += 1
                    self.result.append('Byla použita Ad-hoc rutina číslo 3:')
                    self.result.append('Ze vstupu byl odstraněn token '
                        + removed)

                elif function == '4':
                    """ Diagnostic no. 4: Add '('
                        Adds token [(] into input.
                        Example: (a """
                    token = '[)]'
                    token_number -= 1
                    self.result.append('Byla použita Ad-hoc rutina číslo 4:')
                    self.result.append('Na vstup byl vložen token [)]')

                elif function == '5':
                    """ Diagnostic no. 5: Add '+'
                        Adds token [+] into input.
                        Example: 42 13 """
                    token = '[+]'
                    token_number -= 1
                    self.result.append('Byla použita Ad-hoc rutina číslo 5:')
                    self.result.append('Na vstup byl vložen token [+]')

                # function number 6
                else:
                    self.result.append('Tento stav je nedostupný.')
                    self.exit_code = 1
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
