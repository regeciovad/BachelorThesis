class Scanner(object):

    def get_next_char(self, string):
        """ Return next char of string or error (end of string) """
        try:
            char = next(string)
        except StopIteration:
            char = '[chyba]'
        return char

    def scanner_analysis(self, source_code):
        """ Lexical analysis of source_code """
        # Initialization of variables
        # Source code
        self._code = source_code
        # Output of lexical analysis
        self._scanner = []
        # Iterable source code
        iter_source_code = iter(source_code.rstrip())
        # Actual character from source code
        char = ''
        # Bool variable. If true it will read new character in next loop
        get_new = True
        # Condition for main loop
        run = True
        # Exit code: 0 == ok, 1 == error
        exit_code = 0
        # Main loop
        while(run):
            # Read new char
            if get_new:
                char = self.get_next_char(iter_source_code)
                # In this case error means end of source_code
                if char == '[chyba]':
                    break
            # Comment in source_code
            if char == '{':
                while char != '}':
                    char = self.get_next_char(iter_source_code)
                    # There are no end mark of comment
                    if char == '[chyba]':
                        self._scanner.append('[chyba, chybí }]')
                        exit_code = 1
                        break
                get_new = True
            # Identifiers
            elif char.isalpha():
                lexeme = ''
                while char.isalnum():
                    lexeme = lexeme + char
                    char = self.get_next_char(iter_source_code)
                    if char == '[chyba]':
                        run = False
                        break
                lexeme = lexeme.lower()
                token = '[i, ' + lexeme + ']'
                self._scanner.append(token)
                get_new = False
            # Number
            elif char.isdigit():
                lexeme = ''
                while char.isdigit():
                    lexeme = lexeme + char
                    char = self.get_next_char(iter_source_code)
                    if char == '[chyba]':
                        run = False
                        break
                token = '[#, ' + lexeme + ']'
                self._scanner.append(token)
                get_new = False
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
            # ! or !=
            elif char == '!':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self._scanner.append('[!]')
                elif char == '=':
                    self._scanner.append('[r, !=]')
                    get_new = True
                else:
                    self._scanner.append('[!]')
                    get_new = False
            # In FUN grammar there is only ==, not =
            elif char == '=':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    self._scanner.append('[chyba, neznámý lexém =]')
                    exit_code = 1
                    run = False
                elif char == '=':
                    self._scanner.append('[r, ==]')
                    get_new = True
                else:
                    self._scanner.append('[chyba, neznámý lexém =]')
                    exit_code = 1
                    break
            # > or >=
            elif char == '>':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self._scanner.append('[r, >]')
                elif char == '=':
                    self._scanner.append('[r, >=]')
                    get_new = True
                else:
                    self._scanner.append('[r, >]')
                    get_new = False
            # < or <=
            elif char == '<':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self._scanner.append('[r, <]')
                elif char == '=':
                    self._scanner.append('[r, <=]')
                    get_new = True
                else:
                    self._scanner.append('[r, <]')
                    get_new = False
            # Skipping whitespaces
            elif char.isspace():
                get_new = True
            # Lexeme was not recognized
            else:
                get_new = True
                self._scanner.append('[chyba, neznámý lexém ' + char + ']')
                exit_code = 1
        return self._scanner, exit_code
