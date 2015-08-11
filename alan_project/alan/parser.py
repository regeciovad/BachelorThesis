from .scanner import Scanner
class Parser(object):

	def parser_analysis(self, input):
		#return Scanner._keywords
		for token in input:
			print(token)