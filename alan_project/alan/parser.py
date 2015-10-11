from .scanner import Scanner
from .stack import Stack
from .lrtable import LRTable


class Parser(object):

	def parser_analysis(self, input='', grammar=''):
		output = []
		exit_code = 0
		if input == '':
			output.append('Syntaktická chyba - prázdný program')
			exit_code = 1
			return [], [], output, exit_code
		if grammar == '':
			output.append('Chyba programu - prázdná množina pravidel')
			exit_code = 1
			return [], [], output, exit_code
		if input[-1] != '[$]':
			input.append('[$]')
		stack = Stack()
		stack.push('<$, 0>')
		stackHistory = [stack.get_stack()]
		lrtable = LRTable()
		action, goto = lrtable.generate_table()
		token_number = 0
		state = 0
		stateHistory = [state]
		token = input[token_number]
		token_number += 1
		while (True):
			a = token[1]
			cell = action[state][a]
			output.append('action[' + str(state) + ', ' + a + '] = ' + cell)
			if cell.startswith('s'):
				q = cell[1:]
				stack.push('<'+ a + ', '+ q + '>')
				stackHistory.append(stack.get_stack())
				try:
					token = input[token_number]
					token_number += 1
				except IndexError:
					output.append('syntaktická chyba')
					break
				a = token[1]
				state = int(q)
				stateHistory.append(state)
			elif cell.startswith('r'):
				p = cell[1:]
				left = grammar[int(p)]['left']
				right = grammar[int(p)]['right']
				handle = right.split(' ')
				pop_stack = []
				for x in range(len(handle)):
					pop_stack.append(stack.pop().split(',')[0][1:])
				pop_stack.reverse()
				if str(handle) == str(pop_stack):
					output.append('pravidlo ' + p + ': ' + left + ' -> ' + right)
					stateHistory.append('')
					stackHistory.append('')
					actual_state = int(stack.get_topmost().split(',')[1][:-1])
					if actual_state == '':
						output.append('gotochyba')
						exit_code = 1
						break
					state = int(goto[actual_state][left])
					stateHistory.append(state)
					stack.push(('<'+ left + ', '+ str(state) + '>'))
					stackHistory.append(stack.get_stack())
				else:
					output.append('syntaktická chyba')
					exit_code = 1
					break
			elif cell.startswith('acc'):
				output.append('success')
				stackHistory.append('')
				stateHistory.append('')
				break
			else:
				output.append('syntaktická chyba')
				exit_code = 1
				stackHistory.append('')
				stateHistory.append('')
				break
		return stackHistory, stateHistory, output, exit_code
