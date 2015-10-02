from django.test import TestCase
from .scanner import Scanner
from .stack import Stack
from .parser import Parser
from .models import Rule
from populate_alan_newbie import populate

class ScannerMethodTests(TestCase):

	def test_scanner_empty_program(self):
		'''
			Test of empty program to make sure scanner can handle this.
		'''
		scanner = Scanner()
		output = []
		code = '{Zde je pouze komentar}'
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_comment_without_end(self):
		'''
			Test code of FUN to make sure scanner can detect lexical error - 
			comment without end mark '}'.
		'''
		scanner = Scanner()
		output = ['[chyba, chybí }]']
		with open('files/test_fun_comment.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_double_program(self):
		'''
			Test code of FUN to make sure scanner can detect correct lexems.
			Program Double is just a simple code printing double input value.
		'''
		scanner = Scanner()
		output = ['[i, variable]', '[*]', '[#, 2]'] 
		with open('files/fun_double.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_double_program_cz(self):
		'''
			Program Double with diacritics which should be ignored.

		'''
		scanner = Scanner()
		output = ['[i, variable]', '[*]', '[#, 2]'] 
		with open('files/fun_double_cz.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_relational_operators(self):
		'''
			Program Operators to make sure scanner can recognize every operants
			and doen't miss any character from input.

		'''
		scanner = Scanner()
		output = ['[i, u]', '[r, ==]', '[#, 2]', '[;]', '[i, u]',
		'[*]', '[#, 2]', '[;]','[i, u]', '[r, >]','[#, 2]', '[;]', '[i, u]',
		'[+]', '[#, 4]', '[;]', '[i, u]', '[r, !=]', '[#, 42]', '[;]', '[i, u]',
		'[-]', '[#, 0]', '[;]', '[i, u]', '[r, >=]', '[#, 42]', '[;]', '[i, u]',
		'[/]', '[#, 42]', '[;]', '[i, u]', '[r, <]', '[#, 42]', '[;]', '[i, u]',
		'[*]', '[#, 5]', '[;]', '[i, u]', '[r, <=]', '[#, 42]', '[;]', '[i, u]',
		'[*]', '[#, 5]']
		with open('files/test_fun_operators.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_unknown_char(self):
		'''
			Program Unknown to make sure scanner can correctly 
			find unknow charcter.

		'''
		scanner = Scanner()
		output = ['[i, u]', '[chyba, neznámý lexém @]', '[#, 2]']
		with open('files/test_fun_unknown.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_logical_operators(self):
		'''
			Program to make sure scanner can correctly 
			find logical operators.

		'''
		scanner = Scanner()
		output = ['[i, u]', '[&]', '[i, v]', '[;]', '[i, u]', '[|]', '[i, v]',
		'[;]', '[!]', '[i, result]', '[;]', '[(]', '[i, result]', '[)]']
		with open('files/test_fun_logical_operators.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_id(self):
		'''
			Program to make sure scanner can correctly stop with the end of code.

		'''
		scanner = Scanner()
		output = ['[i, result]']
		with open('files/test_fun_end_id.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_not(self):
		'''
			Program to make sure scanner can correctly stop with the end of code.

		'''
		scanner = Scanner()
		output = ['[i, result]', '[r, ==]', '[!]']
		with open('files/test_fun_end_not.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_bigger(self):
		'''
			Program to make sure scanner can correctly stop with the end of code.

		'''
		scanner = Scanner()
		output = ['[i, result]', '[r, >]']
		with open('files/test_fun_end_bigger.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_smaller(self):
		'''
			Program to make sure scanner can correctly stop with the end of code.

		'''
		scanner = Scanner()
		output = ['[i, result]', '[r, <]']
		with open('files/test_fun_end_smaller.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_equal(self):
		'''
			Program Unknown to make sure scanner can find unknown lexem "=".

		'''
		scanner = Scanner()
		output = ['[i, result]', '[chyba, neznámý lexém =]']
		with open('files/test_fun_end_equal.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_not_equal(self):
		'''
			Program Unknown to make sure scanner can find unknown lexem "=".

		'''
		scanner = Scanner()
		output = ['[i, result]', '[chyba, neznámý lexém =]']
		with open('files/test_fun_not_equal.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)


class StackMethodTests(TestCase):

	def test_stack_init(self):
		'''
			Testing initialization of stack
		'''
		stack = Stack()
		output = []
		stack_output = stack.get_stack()
		self.assertEqual(stack_output, output)

	def test_stack_empty(self):
		'''
			Testing the stack is empty after initialization
		'''
		stack = Stack()
		self.assertTrue(stack.is_empty())

	def test_stack_not_empty(self):
		'''
			Testing the stack is not empty after push() and correction of push
		'''
		stack = Stack()
		stack.push('42')
		output = ['42']
		stack_output = stack.get_stack()
		self.assertEqual(stack_output, output)
		self.assertFalse(stack.is_empty())

	def test_stack_more_push(self):
		'''
			Testing correction of multiple push
		'''
		stack = Stack()
		stack.push('42')
		stack.push('14')
		stack.push('1')
		output = ['42', '14', '1']
		stack_output = stack.get_stack()
		self.assertEqual(stack_output, output)
		self.assertFalse(stack.is_empty())

	def test_stack_one_push_one_pop(self):
		'''
			Testing correction of pop and is_empty
		'''
		stack = Stack()
		stack.push('42')
		output = '42'
		stack_output = stack.pop()
		self.assertEqual(stack_output, output)
		self.assertTrue(stack.is_empty())

	def test_stack_one_push_more_pop(self):
		'''
			Testing correction of pop with empty stack
		'''
		stack = Stack()
		stack.push('42')
		output = '42'
		stack_output = stack.pop()
		self.assertEqual(stack_output, output)
		self.assertTrue(stack.is_empty())
		output = None
		stack_output = stack.pop()
		self.assertEqual(stack_output, output)
		self.assertTrue(stack.is_empty())

	def test_get_topmost_empty(self):
		'''
			Testing correction of get_topmost with empty stack
		'''
		stack = Stack()
		output = None
		stack_output = stack.get_topmost()
		self.assertEqual(stack_output, output)
		self.assertTrue(stack.is_empty())

	def test_get_topmost_one(self):
		'''
			Testing correction of get_topmost with one item on the stack
		'''
		stack = Stack()
		stack.push('42')
		output = '42'
		stack_output = stack.get_topmost()
		self.assertEqual(stack_output, output)
		self.assertFalse(stack.is_empty())

	def test_get_topmost_more(self):
		'''
			Testing correction of get_topmost with more items on the stack
		'''
		stack = Stack()
		stack.push('42')
		stack.push('14')
		stack.push('1')
		output = '1'
		stack_output = stack.get_topmost()
		self.assertEqual(stack_output, output)
		self.assertFalse(stack.is_empty())
		output = ['42', '14', '1']
		stack_output = stack.get_stack()
		self.assertEqual(stack_output, output)

class ParserMethodTests(TestCase):

	def test_parser_empty_code(self):
		'''
			Testing of empty code for parser. It should be error.
		'''
		parser = Parser()
		output = ([], [], ['Syntaktická chyba - prázdný program'])
		parser_output = parser.parser_analysis()
		self.assertEqual(parser_output, output)

	def test_parser_empty_grammar_list(self):
		'''
			Testing of empty list of grammar rules for parser. It should be error.
		'''
		parser = Parser()
		lex_code = '[i, a]'
		output = ([], [], ['Chyba programu - prázdná množina pravidel'])
		parser_output = parser.parser_analysis(lex_code)
		self.assertEqual(parser_output, output)

	def test_parser_a(self):
		'''
			Testing of code: a
		'''
		parser = Parser()
		populate()
		grammar = Rule.objects.order_by('id')
		grammar_list = []
		grammar_list.append({'id':0, 'left':'', 'right':''})
		for g in grammar:
			grammar_list.append({'id':g.id, 'left':g.left_hand_side, 'right':g.right_hand_side})
		lex_code = ['[i, a]']
		stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', ['<$, 0>', '<<factor>, 7>'], '',
			['<$, 0>', '<<term>, 6>'], '', ['<$, 0>', '<<expression>, 5>'], '',
			['<$, 0>', '<<condition>, 3>'], '', ['<$, 0>', '<<statement>, 2>'], '',
			['<$, 0>', '<<statement_list>, 1>'], '']
		state_expected = [0, 9, '', 7, '', 6, '', 5, '', 3, '', 2, '', 1, '']
		output_expected = ['action[0, i] = s9', 'action[9, $] = r16', 'ruled by 16: <factor> -> i',
			'action[7, $] = r14', 'ruled by 14: <term> -> <factor>', 'action[6, $] = r11',
			'ruled by 11: <expression> -> <term>', 'action[5, $] = r8', 
			'ruled by 8: <condition> -> <expression>', 'action[3, $] = r6',
			'ruled by 6: <statement> -> <condition>', 'action[2, $] = r2',
			'ruled by 2: <statement_list> -> <statement>', 'action[1, $] = acc', 'success']
		stack, state, parser_output = parser.parser_analysis(lex_code, grammar_list)
		self.assertEqual(parser_output, output_expected)
		self.assertEqual(stack, stack_expected)
		self.assertEqual(state, state_expected)

	def test_parser_a_less(self):
		'''
			Testing of code: a <, which is a syntax error
		'''
		parser = Parser()
		populate()
		grammar = Rule.objects.order_by('id')
		grammar_list = []
		grammar_list.append({'id':0, 'left':'', 'right':''})
		for g in grammar:
			grammar_list.append({'id':g.id, 'left':g.left_hand_side, 'right':g.right_hand_side})
		lex_code = ['[i, a]', '[r, <]']
		stack_expected = [['<$, 0>'], ['<$, 0>', '<i, 9>'], '', ['<$, 0>', '<<factor>, 7>'], '',
			['<$, 0>', '<<term>, 6>'], '', ['<$, 0>', '<<expression>, 5>'], '',
			['<$, 0>', '<<condition>, 3>'], '', ['<$, 0>', '<<statement>, 2>'],
			['<$, 0>', '<<statement>, 2>', '<r, 12>'], '']
		state_expected = [0, 9, '', 7, '', 6, '', 5, '', 3, '', 2, 12, '']
		output_expected = ['action[0, i] = s9', 'action[9, r] = r16', 'ruled by 16: <factor> -> i',
			'action[7, r] = r14', 'ruled by 14: <term> -> <factor>', 'action[6, r] = r11',
			'ruled by 11: <expression> -> <term>', 'action[5, r] = r8', 
			'ruled by 8: <condition> -> <expression>', 'action[3, r] = r6',
			'ruled by 6: <statement> -> <condition>', 'action[2, r] = s12',
			'action[12, $] = ', 'synchyba']
		stack, state, parser_output = parser.parser_analysis(lex_code, grammar_list)
		self.assertEqual(parser_output, output_expected)
		self.assertEqual(stack, stack_expected)
		self.assertEqual(state, state_expected)

