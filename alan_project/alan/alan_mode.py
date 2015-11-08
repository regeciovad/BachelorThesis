# Advanced Error Recovery during Bottom-Up Parsing
# File: alan_mode.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from .stack import Stack
from .lrtable import LRTable
import time


class AlanModeParser(object):

    def __init__(self):
        # Output of syntax analysis
        self.result = []
        # Output of recovery method Panic Mode
        self.alan_mode_result = []
        # Exit code: 0 == ok, 1 == error
        self.exit_code = 0
        # Stack and it's records
        self.stack = Stack()
        self.stackHistory = []
        # State records
        self.stateHistory = []
        # LR Table
        self.lrtable = LRTable()
        self.alan_time = 0


    def parser_analysis(self, tokens=[], grammar=[]):
        """ Advanced syntax analysis with Alan Mode recovery
            Input: list of tokens, grammar rules
            Output: result of syntax analysis, stack history, state history
                    panic mode recovery records and exit code"""

        self.tokens = tokens
        # List of tokens are missing
        if self.tokens == []:
            self.result.append('Syntaktická chyba - prázdný program')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code, self.alan_mode_result)

        # List of grammar rules are missing
        if grammar == []:
            self.result.append('Chyba programu - prázdná množina pravidel')
            self.exit_code = 1
            return (self.result, self.stackHistory, self.stateHistory,
                    self.exit_code, self.alan_mode_result)
        self.grammar = grammar

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
                except IndexError:
                    self.result.append('syntaktická chyba')
                    break
                a = self.token[1]
                self.state = int(q)
                self.stateHistory.append(self.state)

            # action[state][token] == r(p), p is a number of rule
            # Apply rule, change stack and state
            elif cell.startswith('r'):
                p = cell[1:]
                left = self.grammar[int(p)]['left']
                right = self.grammar[int(p)]['right']
                handle = right.split(' ')
                pop_stack = []
                for x in range(len(handle)):
                    pop_stack.append(self.stack.pop().split(',')[0][1:])
                pop_stack.reverse()
                if str(handle) == str(pop_stack):
                    self.result.append(
                        'pravidlo ' + p + ': ' + left + ' -> ' + right)
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    actual_state = int(
                        self.stack.get_topmost().split(',')[1][:-1])
                    if actual_state == '':
                        self.result.append('gotochyba')
                        self.exit_code = 1
                        break
                    self.state = int(self.goto[actual_state][left])
                    self.result.append('goto[' + str(actual_state) + ', ' + left + '] =' + str(self.state))
                    self.stateHistory.append('')
                    self.stackHistory.append('')
                    self.stateHistory.append(self.state)
                    self.stack.push('<' + left + ', ' + str(self.state) + '>')
                    self.stackHistory.append(self.stack.get_stack())
                else:
                    self.result.append('syntaktická chyba')
                    self.exit_code = 1
                    break

            # action[state][token] == acc, source code is correct
            elif cell.startswith('acc'):
                self.result.append('success')
                self.exit_code = 0
                self.stackHistory.append('')
                self.stateHistory.append('')
                break

            # action[state][token] == blank, source code has some syntax error
            else:
                self.result.append('syntaktická chyba')
                self.result.append('Zahájení zotavovací metody')
                self.result.append('...')
                self.exit_code = 1
                self.stackHistory.append('')
                self.stackHistory.append('')
                self.stackHistory.append('')
                self.stateHistory.append('')
                self.stateHistory.append('')
                self.stateHistory.append('')
                begin = time.clock()
                alan_mode_exit = self.alan_mode()
                end = time.clock()
                mytime = end - begin
                self.alan_mode_result.append("Čas zotavení: %f \u03BCs" % mytime)
                self.alan_mode_result.append('')
                if alan_mode_exit == 1:
                    self.result.append('Syntaktická analýza nemůže dále pokračovat.')
                    break

        # Return results
        return (self.result, self.stackHistory, self.stateHistory,
                self.exit_code, self.alan_mode_result)

    def alan_mode(self):
        """ Alan Mode recovery
                There will be some comment """
        self.alan_mode_result.append(
            'Zahájení Alanova módu.')
        popped = self.stack.pop()
        if str(popped) == '<$, 0>' or popped == None:
            self.alan_mode_result.append(
                'Nenalazen žádný záchytný token.')
            self.alan_mode_result.append(
                'Alanova metoda na tuto chybu nestaci.')
            return 1
        else:
            popped = popped.split(',')[0][1:]

        # Search popped token in right side of rules (reversed order)
        right_side = ''
        for rule in reversed(self.grammar):
            right_side = rule['right']
            if popped in right_side and popped!=rule['left']:
                break
        if right_side == '':
            self.alan_mode_result.append(
                'Nenalazeno žádné vhodné pravidlo.')
            self.alan_mode_result.append(
                'Alanova metoda na tuto chybu nestaci.')
            return 1
        self.alan_mode_result.append("Nalezeno pravidlo: ")
        self.alan_mode_result.append(rule['left'] + " -> " + rule['right'])

        left = rule['left']
        handle = rule['right'].split(' ')
        position = handle.index(popped)

        # position is saying how many token we have to pop from the stack
        for x in range(position):
            check = self.stack.pop()
            if str(check) == '<$, 0>' or check == None:
                self.alan_mode_result.append(
                    'Konec zásobníku.')
                self.alan_mode_result.append(
                    'Alanova metoda na tuto chybu nestaci.')
                return 1
        self.alan_mode_result.append(
            'Zásobník vyprázdněn do: ' + str(self.stack.get_topmost()))

        # Get actual state and find out new state with goto part of tabel
        actual_state = int(self.stack.get_topmost().split(',')[1][:-1])
        self.state = int(self.goto[actual_state][left])
        self.alan_mode_result.append('goto[' + str(actual_state) + ', ' + left + '] =' + str(self.state))
        self.stateHistory.append(self.state)
        self.stack.push('<' + left + ', ' + str(self.state) + '>')
        self.stackHistory.append(self.stack.get_stack())

        
        if left == '<factor>':
            follow = ['$', ';', 'r', '&', '|', '+', '-', ')', '*', '/']
        elif left == '<term>':
            follow = ['$', ';', 'r', '&', '|', '+', '-', ')', '*', '/']
        elif left == '<expression>':
            follow = ['$', ';', 'r', '&', '|', '+', '-', ')']
        elif left == '<condition>':
            follow = ['$', ';', 'r', '&', '|']
        elif left == '<statement>':
            follow = ['$', ';', 'r', '&', '|']
        elif left == '<statement_list>':
            follow = ['$']

        while True:
            if self.token[1] in follow:
                break
            else:
                try:
                    self.token = self.tokens[self.token_number]
                    self.token_number += 1
                except IndexError:
                    self.panic_mode_result.append(
                        'Na vstupu nebyl nalezen žádný symbol z této množiny.')
                    self.panic_mode_result.append(
                        'Panicka metoda na tuto chybu nestaci.')
                    return 1

        self.alan_mode_result.append('Aktualizace stavu: ' + str(self.state))
        self.alan_mode_result.append('Ukončení Alanovi módu.')
        return 0
