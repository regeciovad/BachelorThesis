class Scanner(object):
    _code = ''
    _scanner = []
    _keywords = {'begin', 'declaration', 'else', 'end', 'execution', 'for',
                 'if', 'integer', 'iterate', 'program', 'read', 'then',
                 'through', 'write'}

    def get_next(self, input):
        """ Return next char of input or error """
        try:
            char = next(input)
        except StopIteration:
            char = '[chyba]'
        return char

    def scanner_analysis(self, input):
        """ Lexical analysis of input for FUN grammer """
        self._code = input
        self._scanner = []
        input = input.rstrip()
        iter_input = iter(input)
        char = ''
        get_new = True
        while(True):
            # Read new char
            if get_new:
                char = self.get_next(iter_input)
                # In this case error means end of input
                if char == '[chyba]':
                    return self._scanner
            # Comment in input
            if char == '{':
                while char != '}':
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        self._scanner.append('[chyba, chybi }]')
                        return self._scanner
                get_new = True
            # Identifiers
            elif char.isalpha():
                lexeme = ''
                while char.isalnum():
                    lexeme = lexeme + char
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        self._scanner.append('[chyba, za ' + lexeme + ']')
                        return self._scanner
                lexeme = lexeme.lower()
                if lexeme in self._keywords:
                    token = '[k, ' + lexeme + ']'
                else:
                    token = '[i, ' + lexeme + ']'
                self._scanner.append(token)
                get_new = False
            # Number
            elif char.isdigit():
                lexeme = ''
                while char.isdigit():
                    lexeme = lexeme + char
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        self._scanner.append('[chyba, za ' + lexeme + ']')
                        return self._scanner
                token = '[#, ' + lexeme + ']'
                self._scanner.append(token)
                get_new = False
            # Text literal
            elif char == "'":
                lexeme = ''
                while (True):
                    char = self.get_next(iter_input)
                    if char == '[chyba]':
                        self._scanner.append("[chyba, chybi ']")
                        return self._scanner
                    if char == "'":
                        break
                    lexeme = lexeme + char
                token = '[t, ' + lexeme + ']'
                self._scanner.append(token)
                get_new = True
            elif char == ',':
                self._scanner.append('[,]')
                get_new = True
            elif char == ';':
                self._scanner.append('[;]')
                get_new = True
            elif char == '(':
                self._scanner.append('[(]')
                get_new = True
            elif char == ')':
                self._scanner.append('[)]')
                get_new = True
            elif char == '+':
                self._scanner.append('[+]')
                get_new = True
            elif char == '-':
                self._scanner.append('[-]')
                get_new = True
            elif char == '*':
                self._scanner.append('[*]')
                get_new = True
            elif char == '/':
                self._scanner.append('[/]')
                get_new = True
            elif char == '&':
                self._scanner.append('[&]')
                get_new = True
            elif char == '|':
                self._scanner.append('[|]')
                get_new = True
            elif char == '.':
                self._scanner.append('[.]')
                get_new = True
            elif char == '=':
                char = self.get_next(iter_input)
                if char == '[chyba]':
                    self._scanner.append('[chyba, neukonceny program]')
                    return self._scanner
                if char == '=':
                    self._scanner.append('[r, ==]')
                    get_new = True
                else:
                    self._scanner.append('[=]')
                    get_new = False
            elif char == '!':
                char = self.get_next(iter_input)
                if char == '[chyba]':
                    self._scanner.append('[chyba, neukonceny program]')
                    return self._scanner
                if char == '=':
                    self._scanner.append('[r, !=]')
                    get_new = True
                else:
                    self._scanner.append('[!]')
                    get_new = False
            elif char == '>':
                char = self.get_next(iter_input)
                if char == '[chyba]':
                    self._scanner.append('[chyba, neukonceny program]')
                    return self._scanner
                if char == '=':
                    self._scanner.append('[r, >=]')
                    get_new = True
                else:
                    self._scanner.append('[r, >]')
                    get_new = False
            elif char == '<':
                char = self.get_next(iter_input)
                if char == '[chyba]':
                    self._scanner.append('[chyba, neukonceny program]')
                    return self._scanner
                if char == '=':
                    self._scanner.append('[r, <=]')
                    get_new = True
                else:
                    self._scanner.append('[r, <]')
                    get_new = False
            elif char.isspace():
                get_new = True
            else:
                get_new = True
                self._scanner.append('[chyba, neznami lexem ' + char + ']')
