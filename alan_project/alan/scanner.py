import re

class Scanner(object):
    _code = ''
    _scanner = ''

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
        self._scanner = output
        return output
