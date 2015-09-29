from django.test import TestCase
from .scanner import Scanner

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