#############
# Constants #
#############

DIGITS = '0123456789'

##########
# Tokens #
##########
INT = 'INT'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'


class Token:
    """
    it is a single element of a programming language
    """

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f'{self.type}'


##########
# errors #
##########

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nfile: {self.pos_start.fn}, line: {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


############
# position #
############

class Position:
    """
    keeps track of the line number, column number, current index
    """

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, curr_char):
        self.idx += 1
        self.col += 1

        if curr_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#########
# lexer #
#########

class Lexer:
    """
    it is a component that takes a string as input, then outputs a list of tokens
    """

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.curr_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.curr_char is not None:
            if self.curr_char in ' \t':
                self.advance()
            elif self.curr_char in DIGITS:
                tokens.append(self.make_number())
            elif self.curr_char == '+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.curr_char == '-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.curr_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.curr_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.curr_char
                error_ = IllegalCharError(pos_start, self.pos, char).as_string()
                self.advance()
                return [], error_
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.curr_char is not None and self.curr_char in DIGITS + '.':
            if self.curr_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.curr_char
            self.advance()

        if dot_count == 0:
            return Token(INT, int(num_str))
        else:
            return Token(FLOAT, float(num_str))


#######
# run #
#######

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
