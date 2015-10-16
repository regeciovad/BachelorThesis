# Advanced Error Recovery during Bottom-Up Parsing
# File: scanner.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz


class Scanner:

    def __init__(self):
        # Output of lexical analysis
        self.tokens = []
        # Exit code: 0 == ok, 1 == error
        self.exit_code = 0

    def get_next_char(self, string):
        """ Return next char of string or error (end of string) """
        try:
            char = next(string)
        except StopIteration:
            char = '[chyba]'
        return char

    def scanner_analysis(self, source_code):
        """ Lexical analysis of source_code
            Input: source code of Alan program
            Output: list of tokens and exit code """

        # Iterable source code
        iter_source_code = iter(source_code.rstrip())
        # Actual character from source code
        char = ''
        # Bool variable. If true it will read new character in next loop
        get_new = True
        # Condition for main loop
        run = True

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
                        self.tokens.append('[chyba, chybí }]')
                        self.exit_code = 1
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
                self.tokens.append(token)
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
                self.tokens.append(token)
                get_new = False

            elif char == ';':
                self.tokens.append('[;]')
                get_new = True

            elif char == '(':
                self.tokens.append('[(]')
                get_new = True

            elif char == ')':
                self.tokens.append('[)]')
                get_new = True

            elif char == '+':
                self.tokens.append('[+]')
                get_new = True

            elif char == '-':
                self.tokens.append('[-]')
                get_new = True

            elif char == '*':
                self.tokens.append('[*]')
                get_new = True

            elif char == '/':
                self.tokens.append('[/]')
                get_new = True

            elif char == '&':
                self.tokens.append('[&]')
                get_new = True

            elif char == '|':
                self.tokens.append('[|]')
                get_new = True

            # ! or !=
            elif char == '!':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self.tokens.append('[!]')
                elif char == '=':
                    self.tokens.append('[r, !=]')
                    get_new = True
                else:
                    self.tokens.append('[!]')
                    get_new = False

            # In FUN grammar there is only ==, not =
            elif char == '=':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    self.tokens.append('[chyba, neznámý lexém =]')
                    self.exit_code = 1
                    run = False
                elif char == '=':
                    self.tokens.append('[r, ==]')
                    get_new = True
                else:
                    self.tokens.append('[chyba, neznámý lexém =]')
                    self.exit_code = 1
                    break

            # > or >=
            elif char == '>':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self.tokens.append('[r, >]')
                elif char == '=':
                    self.tokens.append('[r, >=]')
                    get_new = True
                else:
                    self.tokens.append('[r, >]')
                    get_new = False

            # < or <=
            elif char == '<':
                char = self.get_next_char(iter_source_code)
                if char == '[chyba]':
                    run = False
                    self.tokens.append('[r, <]')
                elif char == '=':
                    self.tokens.append('[r, <=]')
                    get_new = True
                else:
                    self.tokens.append('[r, <]')
                    get_new = False

            # Skipping whitespaces
            elif char.isspace():
                get_new = True

            # Lexeme was not recognized
            else:
                get_new = True
                self.tokens.append('[chyba, neznámý lexém ' + char + ']')
                self.exit_code = 1

        return self.tokens, self.exit_code
