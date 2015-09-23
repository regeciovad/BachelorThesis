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
		action.append({"pk":"0", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"1", ";":"", "i":"", "#":"", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"", "$":"acc"})
		action.append({"pk":"2", ";":"s10", "i":"", "#":"", "r":"s11", "+":"", "-":"", "*":"", "/":"", "&":"s12", "|":"s13", "!":"", "(":"", ")":"", "$":"r2"})
		action.append({"pk":"3", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"4", ";":"r7", "i":"", "#":"", "r":"r7", "+":"s15", "-":"s16", "*":"", "/":"", "&":"r7", "|":"r7", "!":"", "(":"", ")":"", "$":"r7"})
		action.append({"pk":"5", ";":"r10", "i":"", "#":"", "r":"r10", "+":"r10", "-":"r10", "*":"s17", "/":"s18", "&":"r10", "|":"r10", "!":"", "(":"", ")":"r10", "$":"r10"})
		action.append({"pk":"6", ";":"r13", "i":"", "#":"", "r":"r13", "+":"r13", "-":"r13", "*":"r13", "/":"r13", "&":"r13", "|":"r13", "!":"", "(":"", ")":"r13", "$":"r13"})
		action.append({"pk":"7", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s7", ")":"", "$":""})
		action.append({"pk":"8", ";":"r15", "i":"", "#":"", "r":"r15", "+":"r15", "-":"r15", "*":"r15", "/":"r15", "&":"r15", "|":"r15", "!":"", "(":"", ")":"r15", "$":"r15"})
		action.append({"pk":"9", ";":"r16", "i":"", "#":"", "r":"r16", "+":"r16", "-":"r16", "*":"r16", "/":"r16", "&":"r16", "|":"r16", "!":"", "(":"", ")":"r16", "$":"r16"})
		action.append({"pk":"10", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"11", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"12", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"13", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"s3", "(":"s7", ")":"", "$":""})
		action.append({"pk":"14", ";":"r6", "i":"", "#":"", "r":"s11/r6", "+":"", "-":"", "*":"", "/":"", "&":"s12/r6", "|":"s13/r6", "!":"", "(":"", ")":"", "$":"r6"})
		action.append({"pk":"15", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s7", ")":"", "$":""})
		action.append({"pk":"16", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s7", ")":"", "$":""})
		action.append({"pk":"17", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s7", ")":"", "$":""})
		action.append({"pk":"18", ";":"", "i":"s8", "#":"s9", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"s7", ")":"", "$":""})
		action.append({"pk":"19", ";":"", "i":"", "#":"", "r":"", "+":"s15", "-":"s16", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"s28", "$":""})
		action.append({"pk":"20", ";":"", "i":"", "#":"", "r":"", "+":"", "-":"", "*":"", "/":"", "&":"", "|":"", "!":"", "(":"", ")":"", "$":"r1"})
		action.append({"pk":"21", ";":"r3", "i":"", "#":"", "r":"s11/r3", "+":"", "-":"", "*":"", "/":"", "&":"s12/r3", "|":"s13/r3", "!":"", "(":"", ")":"", "$":"r3"})
		action.append({"pk":"22", ";":"r4", "i":"", "#":"", "r":"s11/r4", "+":"", "-":"", "*":"", "/":"", "&":"s12/r4", "|":"s13/r4", "!":"", "(":"", ")":"", "$":"r4"})
		action.append({"pk":"23", ";":"r5", "i":"", "#":"", "r":"s11/r5", "+":"", "-":"", "*":"", "/":"", "&":"s12/r5", "|":"s13/r5", "!":"", "(":"", ")":"", "$":"r5"})
		action.append({"pk":"24", ";":"r8", "i":"", "#":"", "r":"r8", "+":"r8", "-":"r8", "*":"s17", "/":"s18", "&":"r8", "|":"r8", "!":"", "(":"", ")":"r8", "$":"r8"})
		action.append({"pk":"25", ";":"r9", "i":"", "#":"", "r":"r9", "+":"r9", "-":"r9", "*":"s17", "/":"s18", "&":"r9", "|":"r9", "!":"", "(":"", ")":"r9", "$":"r9"})
		action.append({"pk":"26", ";":"r11", "i":"", "#":"", "r":"r11", "+":"r11", "-":"r11", "*":"r11", "/":"r11", "&":"r11", "|":"r11", "!":"", "(":"", ")":"r11", "$":"r11"})
		action.append({"pk":"27", ";":"r12", "i":"", "#":"", "r":"r12", "+":"r12", "-":"r12", "*":"r12", "/":"r12", "&":"r12", "|":"r12", "!":"", "(":"", ")":"r12", "$":"r12"})
		action.append({"pk":"28", ";":"r14", "i":"", "#":"", "r":"r14", "+":"r14", "-":"r14", "*":"r14", "/":"r14", "&":"r14", "|":"r14", "!":"", "(":"", ")":"r14", "$":"r14"})

		goto.append({"pk":"0", "<statement_list>":"1", "<condition>":"2", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"1", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"2", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"3", "<statement_list>":"", "<condition>":"14", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"4", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"5", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"6", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"7", "<statement_list>":"", "<condition>":"", "<expression>":"19", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"8", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"9", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"10", "<statement_list>":"20", "<condition>":"2", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"11", "<statement_list>":"", "<condition>":"21", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"12", "<statement_list>":"", "<condition>":"22", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"13", "<statement_list>":"", "<condition>":"23", "<expression>":"4", "<term>":"5", "<factor>":"6"})
		goto.append({"pk":"14", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"15", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"24", "<factor>":"6"})
		goto.append({"pk":"16", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"25", "<factor>":"6"})
		goto.append({"pk":"17", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":"26"})
		goto.append({"pk":"18", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":"27"})
		goto.append({"pk":"19", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"20", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"21", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"22", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"23", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"24", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"25", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"26", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"27", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		goto.append({"pk":"28", "<statement_list>":"", "<condition>":"", "<expression>":"", "<term>":"", "<factor>":""})
		return action, goto

	def generate_table_print(self):
		action = []
		goto = []
		action.append({"pk":"0", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"1", "s":"", "i":"", "h":"", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"", "end":"acc"})
		action.append({"pk":"2", "s":"s10", "i":"", "h":"", "r":"s11", "p":"", "m":"", "t":"", "d":"", "a":"s12", "o":"s13", "n":"", "b":"", "e":"", "end":"r2"})
		action.append({"pk":"3", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"4", "s":"r7", "i":"", "h":"", "r":"r7", "p":"s15", "m":"s16", "t":"", "d":"", "a":"r7", "o":"r7", "n":"", "b":"", "e":"", "end":"r7"})
		action.append({"pk":"5", "s":"r10", "i":"", "h":"", "r":"r10", "p":"r10", "m":"r10", "t":"s17", "d":"s18", "a":"r10", "o":"r10", "n":"", "b":"", "e":"r10", "end":"r10"})
		action.append({"pk":"6", "s":"r13", "i":"", "h":"", "r":"r13", "p":"r13", "m":"r13", "t":"r13", "d":"r13", "a":"r13", "o":"r13", "n":"", "b":"", "e":"r13", "end":"r13"})
		action.append({"pk":"7", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s7", "e":"", "end":""})
		action.append({"pk":"8", "s":"r15", "i":"", "h":"", "r":"r15", "p":"r15", "m":"r15", "t":"r15", "d":"r15", "a":"r15", "o":"r15", "n":"", "b":"", "e":"r15", "end":"r15"})
		action.append({"pk":"9", "s":"r16", "i":"", "h":"", "r":"r16", "p":"r16", "m":"r16", "t":"r16", "d":"r16", "a":"r16", "o":"r16", "n":"", "b":"", "e":"r16", "end":"r16"})
		action.append({"pk":"10", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"11", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"12", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"13", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"s3", "b":"s7", "e":"", "end":""})
		action.append({"pk":"14", "s":"r6", "i":"", "h":"", "r":"s11/r6", "p":"", "m":"", "t":"", "d":"", "a":"s12/r6", "o":"s13/r6", "n":"", "b":"", "e":"", "end":"r6"})
		action.append({"pk":"15", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s7", "e":"", "end":""})
		action.append({"pk":"16", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s7", "e":"", "end":""})
		action.append({"pk":"17", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s7", "e":"", "end":""})
		action.append({"pk":"18", "s":"", "i":"s8", "h":"s9", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"s7", "e":"", "end":""})
		action.append({"pk":"19", "s":"", "i":"", "h":"", "r":"", "p":"s15", "m":"s16", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"s28", "end":""})
		action.append({"pk":"20", "s":"", "i":"", "h":"", "r":"", "p":"", "m":"", "t":"", "d":"", "a":"", "o":"", "n":"", "b":"", "e":"", "end":"r1"})
		action.append({"pk":"21", "s":"r3", "i":"", "h":"", "r":"s11/r3", "p":"", "m":"", "t":"", "d":"", "a":"s12/r3", "o":"s13/r3", "n":"", "b":"", "e":"", "end":"r3"})
		action.append({"pk":"22", "s":"r4", "i":"", "h":"", "r":"s11/r4", "p":"", "m":"", "t":"", "d":"", "a":"s12/r4", "o":"s13/r4", "n":"", "b":"", "e":"", "end":"r4"})
		action.append({"pk":"23", "s":"r5", "i":"", "h":"", "r":"s11/r5", "p":"", "m":"", "t":"", "d":"", "a":"s12/r5", "o":"s13/r5", "n":"", "b":"", "e":"", "end":"r5"})
		action.append({"pk":"24", "s":"r8", "i":"", "h":"", "r":"r8", "p":"r8", "m":"r8", "t":"s17", "d":"s18", "a":"r8", "o":"r8", "n":"", "b":"", "e":"r8", "end":"r8"})
		action.append({"pk":"25", "s":"r9", "i":"", "h":"", "r":"r9", "p":"r9", "m":"r9", "t":"s17", "d":"s18", "a":"r9", "o":"r9", "n":"", "b":"", "e":"r9", "end":"r9"})
		action.append({"pk":"26", "s":"r11", "i":"", "h":"", "r":"r11", "p":"r11", "m":"r11", "t":"r11", "d":"r11", "a":"r11", "o":"r11", "n":"", "b":"", "e":"r11", "end":"r11"})
		action.append({"pk":"27", "s":"r12", "i":"", "h":"", "r":"r12", "p":"r12", "m":"r12", "t":"r12", "d":"r12", "a":"r12", "o":"r12", "n":"", "b":"", "e":"r12", "end":"r12"})
		action.append({"pk":"28", "s":"r14", "i":"", "h":"", "r":"r14", "p":"r14", "m":"r14", "t":"r14", "d":"r14", "a":"r14", "o":"r14", "n":"", "b":"", "e":"r14", "end":"r14"})

		goto.append({"pk":"0", "statement_list":"1", "condition":"2", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"1", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"2", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"3", "statement_list":"", "condition":"14", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"4", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"5", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"6", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"7", "statement_list":"", "condition":"", "expression":"19", "term":"5", "factor":"6"})
		goto.append({"pk":"8", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"9", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"10", "statement_list":"20", "condition":"2", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"11", "statement_list":"", "condition":"21", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"12", "statement_list":"", "condition":"22", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"13", "statement_list":"", "condition":"23", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"14", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"15", "statement_list":"", "condition":"", "expression":"", "term":"24", "factor":"6"})
		goto.append({"pk":"16", "statement_list":"", "condition":"", "expression":"", "term":"25", "factor":"6"})
		goto.append({"pk":"17", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":"26"})
		goto.append({"pk":"18", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":"27"})
		goto.append({"pk":"19", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"20", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"21", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"22", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"23", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"24", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"25", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"26", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"27", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"28", "statement_list":"", "condition":"", "expression":"", "term":"", "factor":""})
		return action, goto