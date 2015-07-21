import re

class Scanner(object):

    def scanner_analysis(self, input):
        input = re.sub(r'\s', '', input)
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
            elif char == 'i':
                output.append('[id,i]')
            elif char == '+':
                output.append('[op,+]')
            elif char == '*':
                output.append('[op,*]')
            elif char == '(':
                output.append('[op,(]')
            elif char == ')':
                output.append('[op,)]')
            else:
                output.append('[chyba]')
        return output
