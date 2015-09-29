from django.test import TestCase
from .scanner import Scanner
from .stack import Stack

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
		output = '[]'
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
		output = "['42']"
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
		output = "['42', '14', '1']"
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
		output = "['42', '14', '1']"
		stack_output = stack.get_stack()
		self.assertEqual(stack_output, output)

