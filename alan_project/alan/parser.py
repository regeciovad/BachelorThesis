from .scanner import Scanner
from .stack import Stack
class Parser(object):

	def parser_analysis(self, input=''):
		stack = Stack()
		action, goto = self.generate_table()
		#myinput = ['[i, a]', '[+]', '[i, b]', '[;]']
		myinput = ['[i, a]']
		output = []
		stack.push('$0')
		state = 0
		for token in myinput:
			a = token[1]
			pokus = action[state][a]
			stack.push(token)
			if pokus == 's8':
				output.append('success')
		return output, stack.get_stack()

	def generate_table(self):
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

		goto.append({"pk":"0", "statement":"1", "condition":"2", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"1", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"2", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"3", "statement":"", "condition":"14", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"4", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"5", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"6", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"7", "statement":"", "condition":"", "expression":"19", "term":"5", "factor":"6"})
		goto.append({"pk":"8", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"9", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"10", "statement":"20", "condition":"2", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"11", "statement":"", "condition":"21", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"12", "statement":"", "condition":"22", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"13", "statement":"", "condition":"23", "expression":"4", "term":"5", "factor":"6"})
		goto.append({"pk":"14", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"15", "statement":"", "condition":"", "expression":"", "term":"24", "factor":"6"})
		goto.append({"pk":"16", "statement":"", "condition":"", "expression":"", "term":"25", "factor":"6"})
		goto.append({"pk":"17", "statement":"", "condition":"", "expression":"", "term":"", "factor":"26"})
		goto.append({"pk":"18", "statement":"", "condition":"", "expression":"", "term":"", "factor":"27"})
		goto.append({"pk":"19", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"20", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"21", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"22", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"23", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"24", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"25", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"26", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"27", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		goto.append({"pk":"28", "statement":"", "condition":"", "expression":"", "term":"", "factor":""})
		return action, goto