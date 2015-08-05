import re

class Scanner(object):
    _code = ''
    _scanner = ''
    _keywords = {'begin', 'declaration', 'else', 'end', 'execution', 'for', 'goto', 'if', 'integer', 'iterate', 
                'label', 'program', 'provided', 'read', 'real', 'then', 'through', 'write'}

    def scanner_analysis(self, input):
        self._code = input
        output = []
        iter_input = iter(input)
        for char in iter_input:
            if char == '{':
                while char != '}':
                    try:
                        char = next(iter_input)
                    except StopIteration:
                        output.append('[chyba]')
                        return output
                continue
            else:
                #output.append('[chyba]')
                output.append(char)
        if 'BEGIN'.lower() in self._keywords:
            output.append('YES')
        self._scanner = output
        return output

    def get_next(self, input):
        try:
            char = next(input)
        except StopIteration:
            char = '[chyba]'
        return char

    def new_scanner(self, input):
        self._code = input
        output = []
        iter_input = iter(input)
        char = ''
        get_new = True
        while(True):
            if get_new:
                char = self.get_next(iter_input)
                if char == '[chyba]':
                    return output
            if char == '{':
                while char != '}':
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        output.append('[Chyba, chybi "}"]')
                        return output
                get_new = False
                continue
            elif char.isalpha():
                lex = ''
                while char.isalnum():
                    lex = lex + char
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        output.append(char)
                        return output
                token = '[i, ' + lex + ']'
                output.append(token)
                get_new = False
            elif char.isdigit():
                lex = ''
                while char.isdigit():
                    lex = lex + char
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        output.append(char)
                        return output
                token = '[#, ' + lex + ']'
                output.append(token)
                get_new = False
            elif char == ';':
                output.append('[;]')
                get_new = True
            else:
                get_new = True
                #output.append('[chyba]')
        return output
