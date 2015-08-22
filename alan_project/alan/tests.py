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
		output = ['[k, program]', '[i, testcomment]', '[;]', '[chyba, chybi }]']
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
		output = ['[k, program]', '[i, double]', '[;]', '[k, integer]', 
		'[i, u]', '[;]', '[k, begin]', '[k, read]', '[(]', '[i, u]', '[)]',
		'[;]', '[i, u]', '[=]', '[i, u]', '[*]', '[#, 2]', '[;]', '[k, write]',
		'[(]', '[i, u]', '[)]', '[;]', '[k, end]', '[.]']
		with open('files/fun_double.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_double_program_cz(self):
		'''
			Program Double with diacritics which should be ignored.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, doublecz]', '[;]', '[k, integer]', 
		'[i, u]', '[;]', '[k, begin]', '[k, read]', '[(]', '[i, u]', '[)]',
		'[;]', '[i, u]', '[=]', '[i, u]', '[*]', '[#, 2]', '[;]', '[k, write]',
		'[(]', '[i, u]', '[)]', '[;]', '[k, end]', '[.]']
		with open('files/fun_double_cz.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_string_program(self):
		'''
			Program String which prints 'Hello World!'

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, string]', '[;]', '[k, begin]', 
		'[k, write]', '[(]', '[t, Hello World!]', '[)]', '[;]', '[k, end]', 
		'[.]']
		with open('files/fun_string.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_string_program_without_end(self):
		'''
			Program String without end mark '.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, string]', '[;]', '[k, begin]', 
		'[k, write]', '[(]', "[chyba, chybi ']"]
		with open('files/test_fun_string_less.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_string_program_with_more_ends(self):
		'''
			Program String with more end marks.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, string]', '[;]', '[k, begin]', 
		'[k, write]', '[(]', '[t, Hello ]', '[i, world]', '[!]',
		"[chyba, chybi ']"]
		with open('files/test_fun_string_more.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_relational_operators(self):
		'''
			Program Operators to make sure scanner can recognize every operants
			and doen't miss any character from input.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, operators]', '[;]', '[k, integer]', 
		'[i, u]', '[;]', '[k, begin]', '[k, read]', '[(]', '[i, u]', '[)]',
		'[;]', '[k, if]', '[i, u]', '[r, ==]', '[#, 2]', '[k, then]', '[i, u]',
		'[=]', '[i, u]', '[*]', '[#, 2]', '[;]', '[k, if]', '[i, u]', '[r, >]',
		'[#, 2]', '[k, then]', '[i, u]', '[=]', '[i, u]', '[+]', '[#, 4]',
		'[;]', '[k, if]', '[i, u]', '[r, !=]', '[#, 42]', '[k, then]', '[i, u]',
		'[=]', '[i, u]', '[-]', '[#, 0]', '[;]', '[k, if]', '[i, u]', '[r, >=]',
		'[#, 42]', '[k, then]', '[i, u]', '[=]', '[i, u]', '[/]', '[#, 42]',
		'[;]', '[k, if]', '[i, u]', '[r, <]', '[#, 42]', '[k, then]', '[i, u]',
		'[=]', '[i, u]', '[*]', '[#, 5]', '[;]', '[k, if]', '[i, u]', '[r, <=]',
		'[#, 42]', '[k, then]', '[i, u]', '[=]', '[i, u]', '[*]', '[#, 5]',
		'[;]', '[k, write]', '[(]', '[i, u]', '[)]', '[;]', '[k, end]', '[.]']
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
		output = ['[k, program]', '[i, unknown]', '[;]', '[k, integer]',
		'[i, u]', '[;]', '[k, begin]', '[k, read]', '[(]', '[i, u]', '[)]',
		'[;]', '[i, u]', '[=]', '[i, u]', '[chyba, neznami lexem @]', '[#, 2]',
		'[;]', '[k, write]', '[(]', '[i, u]', '[)]', '[;]', '[k, end]', '[.]']
		with open('files/test_fun_unknown.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_logical_operators(self):
		'''
			Program Unknown to make sure scanner can correctly 
			find logical operators.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, logic]', '[;]', '[k, integer]', '[i, u]',
		'[,]', '[i, v]', '[,]', '[i, result]', '[;]', '[k, begin]',
		'[i, result]', '[=]', '[i, u]', '[&]', '[i, v]', '[;]', '[i, result]',
		'[=]', '[i, u]', '[|]', '[i, v]', '[;]', '[i, result]', '[=]', '[!]', 
		'[i, result]', '[;]', '[k, write]', '[(]', '[i, result]', '[)]', '[;]',
		'[k, end]', '[.]']
		with open('files/test_fun_logical_operators.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_id(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[chyba, za result]']
		with open('files/test_fun_end_id.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_number(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[i, result]', '[;]', '[k, begin]', '[i, result]', '[=]', 
		'[chyba, za 42]']
		with open('files/test_fun_end_number.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_equal(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[i, result]', '[;]', '[k, begin]', '[i, result]',
		'[chyba, neukonceny program]']
		with open('files/test_fun_end_equal.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_not(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[i, result]', '[;]', '[k, begin]', '[i, result]', '[=]',
		'[chyba, neukonceny program]']
		with open('files/test_fun_end_not.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_bigger(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[i, result]', '[;]', '[k, begin]', '[i, result]',
		'[chyba, neukonceny program]']
		with open('files/test_fun_end_bigger.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)

	def test_scanner_end_smaller(self):
		'''
			Program Unknown to make sure scanner can find wrong end of code.

		'''
		scanner = Scanner()
		output = ['[k, program]', '[i, number]', '[;]', '[k, integer]',
		'[i, result]', '[;]', '[k, begin]', '[i, result]',
		'[chyba, neukonceny program]']
		with open('files/test_fun_end_smaller.txt') as f:
			code = f.read()
		lex_code = scanner.scanner_analysis(code)
		self.assertEqual(lex_code, output)
