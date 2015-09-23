from .scanner import Scanner
from .stack import Stack
class Parser(object):

	def parser_analysis(self, input='', grammar=''):
		if input[-1] != '[$]':
			input.append('[$]')
		stack = Stack()
		stack.push('<$, 0>')
		stackHistory = [stack.get_stack()]
		action, goto = self.generate_table()
		token_number = 0
		output = []
		state = 0
		stateHistory = [state]
		run = True
		try:
			token = input[token_number]
			token_number += 1
		except IndexError:
		# In this case error means end of input
			return stackHistory, stateHistory, output
		while (run):
			a = token[1]
			print(state)
			print(stack.get_stack())
			cell = action[int(state)][a]
			output.append('action[' + str(state) + ', ' + a + '] = ' + cell)
			if cell.startswith('s'):
				q = cell[1:]
				stack.push('<'+ a + ', '+ q + '>')
				stackHistory.append(stack.get_stack())
				try:
					token = input[token_number]
					token_number += 1
				except IndexError:
					output.append('chyba')
					break
				a = token[1]
				state = q
				stateHistory.append(q)
			elif cell.startswith('r'):
				p = cell[1:]
				left = grammar[int(p)]['left']
				right = grammar[int(p)]['right']
				handle = right.split(' ')
				pop_stack = []
				for x in range(len(handle)):
					pop_stack.append(stack.pop().split(',')[0][1:])
				pop_stack.reverse()
				print(str(pop_stack))
				if str(handle) == str(pop_stack):
					output.append('ruled by ' + p + ': ' + left + ' -> ' + right)
					stateHistory.append('')
					stackHistory.append('')
					actual_state = stack.get_topmost().split(',')[1][:-1]
					if actual_state == '':
						output.append('gotochyba')
						run = False
					state = goto[int(actual_state)][left]
					stateHistory.append(state)
					stack.push(('<'+ left + ', '+ state + '>'))
					stackHistory.append(stack.get_stack())
				else:
					output.append('chyba')
					run = False
			elif cell.startswith('acc'):
				output.append('success')
				stackHistory.append('')
				stateHistory.append('')
				run = False
			else:
				output.append('synchyba')
				stackHistory.append('')
				stateHistory.append('')
				run = False
		return stackHistory, stateHistory, output


	def generate_table(self):
		action = []
		goto = []
		action.append({"pk":"0", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"1", ";":"", "i":"", "#":"", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"", "$":"acc"})
		action.append({"pk":"2", ";":"s11", "i":"", "#":"", "r":"s12", "+":"", "-":"", "*":"", "/":"", "&":"s13", "|":"s14", "!":"", "(":"", ")":"", "$":"r2"})
		action.append({"pk":"3", ";":"r6", "i":"", "#":"", "r":"r6", "+":"", "-":"", "*":"", "/":"", "&":"r6", "|":"r6", "!":"", "(":"", ")":"", "$":"r6"})
		action.append({"pk":"4", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"5", ";":"r8", "i":"", "#":"", "r":"r8", "+":"s16", "-":"s17", "*":"", "/":"", "&":"r8", "|":"r8", "!":"", "(":"", ")":"", "$":"r8"})
		action.append({"pk":"6", ";":"r11", "i":"", "#":"", "r":"r11", "+":"r11", "-":"r11", "*":"s18", "/":"s19", "&":"r11", "|":"r11", "!":"", "(":"", ")":"r11", "$":"r11"})
		action.append({"pk":"7", ";":"r14", "i":"", "#":"", "r":"r14", "+":"r14", "-":"r14", "*":"r14", "/":"r14", "&":"r14", "|":"r14", "!":"", "(":"", ")":"r14", "$":"r14"})
		action.append({"pk":"8", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s8", ")":"", "$":""})
		action.append({"pk":"9", ";":"r16", "i":"", "#":"", "r":"r16", "+":"r16", "-":"r16", "*":"r16", "/":"r16", "&":"r16", "|":"r16", "!":"", "(":"", ")":"r16", "$":"r16"})
		action.append({"pk":"10", ";":"r17", "i":"", "#":"", "r":"r17", "+":"r17", "-":"r17", "*":"r17", "/":"r17", "&":"r17", "|":"r17", "!":"", "(":"", ")":"r17", "$":"r17"})
		action.append({"pk":"11", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"12", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"13", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"14", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s4", "(":"s8", ")":"", "$":""})
		action.append({"pk":"15", ";":"r7", "i":"", "#":"", "r":"r7", "+":"", "-":"", "*":"", "/":"", "&":"r7", "|":"r7", "!":"", "(":"", ")":"", "$":"r7"})
		action.append({"pk":"16", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s8", ")":"", "$":""})
		action.append({"pk":"17", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s8", ")":"", "$":""})
		action.append({"pk":"18", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s8", ")":"", "$":""})
		action.append({"pk":"19", ";":"", "i":"s9", "#":"s10", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s8", ")":"", "$":""})
		action.append({"pk":"20", ";":"", "i":"", "#":"", "r":"", "+":"s16", "-":"s17", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"s29", "$":""})
		action.append({"pk":"21", ";":"", "i":"", "#":"", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"", "$":"r1"})
		action.append({"pk":"22", ";":"r3", "i":"", "#":"", "r":"r3", "+":"", "-":"", "*":"", "/":"", "&":"r3", "|":"r3", "!":"", "(":"", ")":"", "$":"r3"})
		action.append({"pk":"23", ";":"r4", "i":"", "#":"", "r":"r4", "+":"", "-":"", "*":"", "/":"", "&":"r4", "|":"r4", "!":"", "(":"", ")":"", "$":"r4"})
		action.append({"pk":"24", ";":"r5", "i":"", "#":"", "r":"r5", "+":"", "-":"", "*":"", "/":"", "&":"r5", "|":"r5", "!":"", "(":"", ")":"", "$":"r5"})
		action.append({"pk":"25", ";":"r9", "i":"", "#":"", "r":"r9", "+":"r9", "-":"r9", "*":"s18", "/":"s19", "&":"r9", "|":"r9", "!":"", "(":"", ")":"r9", "$":"r9"})
		action.append({"pk":"26", ";":"r10", "i":"", "#":"", "r":"r10", "+":"r10", "-":"r10", "*":"s18", "/":"s19", "&":"r10", "|":"r10", "!":"", "(":"", ")":"r10", "$":"r10"})
		action.append({"pk":"27", ";":"r12", "i":"", "#":"", "r":"r12", "+":"r12", "-":"r12", "*":"r12", "/":"r12", "&":"r12", "|":"r12", "!":"", "(":"", ")":"r12", "$":"r12"})
		action.append({"pk":"28", ";":"r13", "i":"", "#":"", "r":"r13", "+":"r13", "-":"r13", "*":"r13", "/":"r13", "&":"r13", "|":"r13", "!":"", "(":"", ")":"r13", "$":"r13"})
		action.append({"pk":"29", ";":"r15", "i":"", "#":"", "r":"r15", "+":"r15", "-":"r15", "*":"r15", "/":"r15", "&":"r15", "|":"r15", "!":"", "(":"", ")":"r15", "$":"r15"})

		goto.append({"pk":"0", "<statement_list>":"1", "<statement>":"2", "<condition>":"3", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"1", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"2", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"3", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"4", "<statement_list>":"", "<statement>":"", "<condition>":"15", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"5", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"6", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"7", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"8", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"20", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"9", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"10", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"11", "<statement_list>":"21", "<statement>":"2", "<condition>":"3", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"12", "<statement_list>":"", "<statement>":"", "<condition>":"22", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"13", "<statement_list>":"", "<statement>":"", "<condition>":"23", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"14", "<statement_list>":"", "<statement>":"", "<condition>":"24", "<expression>":"5", "<term>":"6", "<factor>":"7"})
		goto.append({"pk":"15", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"16", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"25", "<factor>":"7"})
		goto.append({"pk":"17", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"26", "<factor>":"7"})
		goto.append({"pk":"18", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":"27"})
		goto.append({"pk":"19", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":"28"})
		goto.append({"pk":"20", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"21", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"22", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"23", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"24", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"25", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"26", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"27", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"28", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"29", "<statement_list>":"", "<statement>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		return action, goto

	def generate_table_print(self):
		action = []
		goto = []
		action.append({"pk":"0", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"1", "s":"", "i":"", "h":"", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"", "end":"acc"})
		action.append({"pk":"2", "s":"s11", "i":"", "h":"", "r":"s12", "p":"", "m":"", "t":"", "d":"", "a":"s13", "o":"s14", "n":"", "b":"", "e":"", "end":"r2"})
		action.append({"pk":"3", "s":"r6", "i":"", "h":"", "r":"r6", "p":"", "m":"", "t":"", "d":"", "a":"r6", "o":"r6", "n":"", "b":"", "e":"", "end":"r6"})
		action.append({"pk":"4", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"5", "s":"r8", "i":"", "h":"", "r":"r8", "p":"s16", "m":"s17", "t":"", "d":"", "a":"r8", "o":"r8", "n":"", "b":"", "e":"", "end":"r8"})
		action.append({"pk":"6", "s":"r11", "i":"", "h":"", "r":"r11", "p":"r11", "m":"r11", "t":"s18", "d":"s19", "a":"r11", "o":"r11", "n":"", "b":"", "e":"r11", "end":"r11"})
		action.append({"pk":"7", "s":"r14", "i":"", "h":"", "r":"r14", "p":"r14", "m":"r14", "t":"r14", "d":"r14", "a":"r14", "o":"r14", "n":"", "b":"", "e":"r14", "end":"r14"})
		action.append({"pk":"8", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s8", "e":"", "end":""})
		action.append({"pk":"9", "s":"r16", "i":"", "h":"", "r":"r16", "p":"r16", "m":"r16", "t":"r16", "d":"r16", "a":"r16", "o":"r16", "n":"", "b":"", "e":"r16", "end":"r16"})
		action.append({"pk":"10", "s":"r17", "i":"", "h":"", "r":"r17", "p":"r17", "m":"r17", "t":"r17", "d":"r17", "a":"r17", "o":"r17", "n":"", "b":"", "e":"r17", "end":"r17"})
		action.append({"pk":"11", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"12", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"13", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"14", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s4", "b":"s8", "e":"", "end":""})
		action.append({"pk":"15", "s":"r7", "i":"", "h":"", "r":"r7", "p":"", "m":"", "t":"", "d":"", "a":"r7", "o":"r7", "n":"", "b":"", "e":"", "end":"r7"})
		action.append({"pk":"16", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s8", "e":"", "end":""})
		action.append({"pk":"17", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s8", "e":"", "end":""})
		action.append({"pk":"18", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s8", "e":"", "end":""})
		action.append({"pk":"19", "s":"", "i":"s9", "h":"s10", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s8", "e":"", "end":""})
		action.append({"pk":"20", "s":"", "i":"", "h":"", "r":"", "p":"s16", "m":"s17", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"s29", "end":""})
		action.append({"pk":"21", "s":"", "i":"", "h":"", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"", "end":"r1"})
		action.append({"pk":"22", "s":"r3", "i":"", "h":"", "r":"r3", "p":"", "m":"", "t":"", "d":"", "a":"r3", "o":"r3", "n":"", "b":"", "e":"", "end":"r3"})
		action.append({"pk":"23", "s":"r4", "i":"", "h":"", "r":"r4", "p":"", "m":"", "t":"", "d":"", "a":"r4", "o":"r4", "n":"", "b":"", "e":"", "end":"r4"})
		action.append({"pk":"24", "s":"r5", "i":"", "h":"", "r":"r5", "p":"", "m":"", "t":"", "d":"", "a":"r5", "o":"r5", "n":"", "b":"", "e":"", "end":"r5"})
		action.append({"pk":"25", "s":"r9", "i":"", "h":"", "r":"r9", "p":"r9", "m":"r9", "t":"s18", "d":"s19", "a":"r9", "o":"r9", "n":"", "b":"", "e":"r9", "end":"r9"})
		action.append({"pk":"26", "s":"r10", "i":"", "h":"", "r":"r10", "p":"r10", "m":"r10", "t":"s18", "d":"s19", "a":"r10", "o":"r10", "n":"", "b":"", "e":"r10", "end":"r10"})
		action.append({"pk":"27", "s":"r12", "i":"", "h":"", "r":"r12", "p":"r12", "m":"r12", "t":"r12", "d":"r12", "a":"r12", "o":"r12", "n":"", "b":"", "e":"r12", "end":"r12"})
		action.append({"pk":"28", "s":"r13", "i":"", "h":"", "r":"r13", "p":"r13", "m":"r13", "t":"r13", "d":"r13", "a":"r13", "o":"r13", "n":"", "b":"", "e":"r13", "end":"r13"})
		action.append({"pk":"29", "s":"r15", "i":"", "h":"", "r":"r15", "p":"r15", "m":"r15", "t":"r15", "d":"r15", "a":"r15", "o":"r15", "n":"", "b":"", "e":"r15", "end":"r15"})

		goto.append({"pk":"0", "statement_list":"1", "statement":"2", "condition":"3", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"1", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"2", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"3", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"4", "statement_list":"", "statement":"", "condition":"15", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"5", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"6", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"7", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"8", "statement_list":"", "statement":"", "condition":"", "expression":"20", "term":"6", "factor":"7"})
		goto.append({"pk":"9", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"10", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"11", "statement_list":"21", "statement":"2", "condition":"3", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"12", "statement_list":"", "statement":"", "condition":"22", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"13", "statement_list":"", "statement":"", "condition":"23", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"14", "statement_list":"", "statement":"", "condition":"24", "expression":"5", "term":"6", "factor":"7"})
		goto.append({"pk":"15", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"16", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"25", "factor":"7"})
		goto.append({"pk":"17", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"26", "factor":"7"})
		goto.append({"pk":"18", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":"27"})
		goto.append({"pk":"19", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":"28"})
		goto.append({"pk":"20", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"21", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"22", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"23", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"24", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"25", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"26", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"27", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"28", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"29", "statement_list":"", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		return action, goto