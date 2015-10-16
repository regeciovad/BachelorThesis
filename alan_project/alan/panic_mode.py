# Advanced Error Recovery during Bottom-Up Parsing
# File: panic_mode.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from .scanner import Scanner
from .stack import Stack
from .lrtable import LRTable


class PanicModeParser(object):

	def parser_analysis(self, input='', grammar=''):
		self.output = []
		self.input = input
		exit_code = 0
		self.panic_mode_output = []
		if self.input == '':
			self.output.append('Syntaktická chyba - prázdný program')
			exit_code = 1
			return [], [], self.output, exit_code, []
		if grammar == '':
			self.output.append('Chyba programu - prázdná množina pravidel')
			exit_code = 1
			return [], [], self.output, exit_code, []
		if self.input[-1] != '[$]':
			self.input.append('[$]')
		self.stack = Stack()
		self.stack.push('<$, 0>')
		stackHistory = [self.stack.get_stack()]
		lrtable = LRTable()
		self.action, self.goto = lrtable.generate_table()
		self.token_number = 0
		self.state = 0
		stateHistory = [self.state]
		self.token = self.input[self.token_number]
		self.token_number += 1
		while True:
			a = self.token[1]
			cell = self.action[self.state][a]
			self.output.append('action[' + str(self.state) + ', ' + a + '] = ' + cell)
			if cell.startswith('s'):
				q = cell[1:]
				self.stack.push('<'+ a + ', '+ q + '>')
				stackHistory.append(self.stack.get_stack())
				try:
					self.token = self.input[self.token_number]
					self.token_number += 1
				except IndexError:
					self.output.append('syntaktická chyba')
					break
				a = self.token[1]
				self.state = int(q)
				stateHistory.append(self.state)
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
					self.output.append('pravidlo ' + p + ': ' + left + ' -> ' + right)
					stateHistory.append('')
					stackHistory.append('')
					actual_state = int(self.stack.get_topmost().split(',')[1][:-1])
					if actual_state == '':
						self.output.append('gotochyba')
						exit_code = 1
						break
					self.state = int(self.goto[actual_state][left])
					stateHistory.append(self.state)
					self.stack.push(('<'+ left + ', '+ str(self.state) + '>'))
					stackHistory.append(self.stack.get_stack())
				else:
					self.output.append('syntaktická chyba')
					exit_code = 1
					break
			elif cell.startswith('acc'):
				self.output.append('success')
				stackHistory.append('')
				stateHistory.append('')
				break
			else:
				self.output.append('syntaktická chyba')
				exit_code = 1
				stackHistory.append('')
				stateHistory.append('')
				self.panic_mode()
				stackHistory.append(self.stack.get_stack())
		return stackHistory, stateHistory, self.output, exit_code, self.panic_mode_output

	def panic_mode(self):
		self.panic_mode_output.append('Zahájení panického módu.')
		synchronization_tokens = ['<expression>', '<condition>', '<statement>', '<statement_list>']
		while True:
			poped = self.stack.pop()
			if poped.split(',')[0][1:] in synchronization_tokens:
				break
		self.panic_mode_output.append('Zásobník vyprázdněn až po: ' + str(self.stack.get_stack()))
		self.panic_mode_output.append('Nalezen neterminál: ' + poped.split(',')[0][1:])
		if poped.split(',')[0][1:] == '<expression>':
			follow = ['$', ';', 'r', '&', '|', '+', '-', ')']
			next = '<condition>'
		elif poped.split(',')[0][1:] == '<condition>':
			follow = ['$', ';', 'r', '&', '|']
			next = '<statement>'
		elif poped.split(',')[0][1:] == '<statement>':
			follow = ['$', ';', 'r', '&', '|']
			next = '<statement_list>'
		elif poped.split(',')[0][1:] == '<statement_list>':
			follow = ['$']
			next = '<statement_list>'
		self.panic_mode_output.append('Aktuální vstup: ' + str(self.input[self.token_number-1:]))
		self.panic_mode_output.append('Hledáme symbol z množiny follow(' + next + '): ' + str(follow))
		while True:
			if self.token[1] in follow:
				break
			else:
				self.token = self.input[self.token_number]
				self.token_number += 1
		self.panic_mode_output.append('Nalezen symbol: ' + str(self.token))
		state = int(self.stack.get_topmost().split(',')[1][:-1])
		self.state = int(self.goto[state][next])
		self.panic_mode_output.append('goto[' + str(state) + ', ' + str(next) + '] = ' + str(self.state))
		self.stack.push('<' + str(next) + ', ' + str(self.state) + '>')
		self.panic_mode_output.append('Vloženo na zásobník: ' + '<' + str(next) + ', ' + str(self.state) + '>')
		self.panic_mode_output.append('Ukončení panického módu.')
		self.panic_mode_output.append('')
