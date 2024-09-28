import sys
from enum import Enum

class TOKEN_TYPE(Enum):
    NONE = -2
    EOF = -1
    STRING = 0
    NUMBER = 1
    IDENTIFIER = 2
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    LEFT_BRACE = 5
    RIGHT_BRACE = 6
    COMMA = 7
    DOT = 8
    MINUS = 9
    PLUS = 10
    SEMICOLON = 11
    STAR = 12
    SLASH = 13
    EQUAL_EQUAL = 14
    EQUAL = 15
    BANG_EQUAL = 16
    BANG = 17
    LESS_EQUAL = 18
    LESS = 19
    GREATER_EQUAL = 20
    GREATER = 21
    AND = 22
    OR = 23
    IF = 24
    ELSE = 25
    FOR = 26
    WHILE = 27
    TRUE = 28
    FALSE = 29
    CLASS = 30
    SUPER = 31
    THIS = 32
    VAR = 33
    FUN = 34
    RETURN = 35
    PRINT = 36
    NIL = 37

class Token:
    def __init__(self, type: TOKEN_TYPE, name: str, value):
        self.type = type
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.type.name} {self.name} {self.value}"

class Lexer:
    def __init__(self, program: str):
        self.program = program
        self.size = len(self.program)
        self.i = 0
        self.line = 1
        self.current_char = self.program[self.i] if self.size > 0 else ""
        self.had_error = False

    def advance(self):
        self.i += 1
        if self.i < self.size:
            self.current_char = self.program[self.i]
        else:
            self.current_char = ""

    def skip_whitespace(self):
        while self.i < self.size and self.current_char.isspace():
            if self.current_char == "\n":
                self.line += 1
            self.advance()

    def next_token(self) -> Token:
        self.skip_whitespace()
        if self.i >= self.size:
            return Token(TOKEN_TYPE.EOF, "", "null")

        char = self.current_char

        if char == "(":
            return self.advance_with(Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"))
        elif char == ")":
            return self.advance_with(Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"))
        elif char == "{":
            return self.advance_with(Token(TOKEN_TYPE.LEFT_BRACE, "{", "null"))
        elif char == "}":
            return self.advance_with(Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null"))
        elif char == ",":
            return self.advance_with(Token(TOKEN_TYPE.COMMA, ",", "null"))
        elif char == ".":
            return self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null"))
        elif char == "-":
            return self.advance_with(Token(TOKEN_TYPE.MINUS, "-", "null"))
        elif char == "+":
            return self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null"))
        elif char == ";":
            return self.advance_with(Token(TOKEN_TYPE.SEMICOLON, ";", "null"))
        elif char == "*":
            return self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null"))
        elif char == "/":
            self.advance()
            if self.current_char == "/":
                while self.current_char != "\n" and self.i < self.size:
                    self.advance()
                return self.next_token()  # Skip to next token after comment
            return Token(TOKEN_TYPE.SLASH, "/", "null")
        elif char == "=":
            self.advance()
            if self.current_char == "=":
                return self.advance_with(Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null"))
            return Token(TOKEN_TYPE.EQUAL, "=", "null")
        elif char == "!":
            self.advance()
            if self.current_char == "=":
                return self.advance_with(Token(TOKEN_TYPE.BANG_EQUAL, "!=", "null"))
            return Token(TOKEN_TYPE.BANG, "!", "null")
        elif char == "<":
            self.advance()
            if self.current_char == "=":
                return self.advance_with(Token(TOKEN_TYPE.LESS_EQUAL, "<=", "null"))
            return Token(TOKEN_TYPE.LESS, "<", "null")
        elif char == ">":
            self.advance()
            if self.current_char == "=":
                return self.advance_with(Token(TOKEN_TYPE.GREATER_EQUAL, ">=", "null"))
            return Token(TOKEN_TYPE.GREATER, ">", "null")
        elif char == '"':
            return self.next_string()
        elif char.isalpha() or char == "_":
            return self.next_id()
        elif char.isdigit():
            return self.next_number()
        else:
            print(f"[line {self.line}] Error: Unexpected character: {char}", file=sys.stderr)
            self.had_error = True
            self.advance()
            return Token(TOKEN_TYPE.NONE, "", "null")
    
    def advance_with(self, token: Token) -> Token:
        self.advance()
        return token

    def next_id(self) -> Token:
        id_str = ""
        while self.i < self.size and (self.current_char.isalnum() or self.current_char == "_"):
            id_str += self.current_char
            self.advance()
        
        match id_str:
            case "and": return Token(TOKEN_TYPE.AND, id_str, "null")
            case "or": return Token(TOKEN_TYPE.OR, id_str, "null")
            case "if": return Token(TOKEN_TYPE.IF, id_str, "null")
            case "else": return Token(TOKEN_TYPE.ELSE, id_str, "null")
            case "for": return Token(TOKEN_TYPE.FOR, id_str, "null")
            case "while": return Token(TOKEN_TYPE.WHILE, id_str, "null")
            case "true": return Token(TOKEN_TYPE.TRUE, id_str, "null")
            case "false": return Token(TOKEN_TYPE.FALSE, id_str, "null")
            case "class": return Token(TOKEN_TYPE.CLASS, id_str, "null")
            case "super": return Token(TOKEN_TYPE.SUPER, id_str, "null")
            case "this": return Token(TOKEN_TYPE.THIS, id_str, "null")
            case "var": return Token(TOKEN_TYPE.VAR, id_str, "null")
            case "fun": return Token(TOKEN_TYPE.FUN, id_str, "null")
            case "return": return Token(TOKEN_TYPE.RETURN, id_str, "null")
            case "print": return Token(TOKEN_TYPE.PRINT, id_str, "null")
            case "nil": return Token(TOKEN_TYPE.NIL, id_str, "null")
        
        return Token(TOKEN_TYPE.IDENTIFIER, id_str, "null")

    def next_string(self) -> Token:
        string_value = ""
        self.advance()  # Skip the opening quote
        start_line = self.line
        while self.current_char != '"':
            if self.i >= self.size:
                print(f"[line {start_line}] Error: Unterminated string.", file=sys.stderr)
                self.had_error = True
                return Token(TOKEN_TYPE.NONE, "", "null")
            if self.current_char == "\n":
                self.line += 1
            string_value += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token(TOKEN_TYPE.STRING, f'"{string_value}"', string_value)

    def next_number(self) -> Token:
        num_str = ""
        dot = False
        while self.i < self.size:
            if self.current_char == ".":
                if dot:
                    break  # Only one dot allowed
                dot = True
            elif not self.current_char.isdigit():
                break
            num_str += self.current_char
            self.advance()
        return Token(TOKEN_TYPE.NUMBER, num_str, float(num_str) if num_str else 0.0)

class Expression:
    pass

class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, str):
            return self.value
        elif self.value is True:
            return "true"
        elif self.value is False:
            return "false"
        elif self.value is None:
            return "nil"
        else:
            return str(self.value)

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator.name} {self.right})"

class Group(Expression):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"(group {self.expression})"

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def parse(self):
        return self.expression()

    def expression(self):
        if self.current_token.type == TOKEN_TYPE.LEFT_PAREN:
            self.consume(TOKEN_TYPE.LEFT_PAREN)
            expr = self.expression()
            self.consume(TOKEN_TYPE.RIGHT_PAREN)
            return Group(expr)
        elif self.current_token.type in [TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING, TOKEN_TYPE.TRUE, TOKEN_TYPE.FALSE, TOKEN_TYPE.NIL]:
            return self.literal()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def unary(self):
        if self.current_token.type in [TOKEN_TYPE.MINUS, TOKEN_TYPE.BANG]:
            operator = self.current_token
            self.consume(self.current_token.type)
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.current_token.type == TOKEN_TYPE.LEFT_PAREN:
            self.consume(TOKEN_TYPE.LEFT_PAREN)
            expr = self.expression()
            self.consume(TOKEN_TYPE.RIGHT_PAREN)
            return Group(expr)
        elif self.current_token.type in [TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING, TOKEN_TYPE.TRUE, TOKEN_TYPE.FALSE, TOKEN_TYPE.NIL]:
            return self.literal()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def literal(self):
        if self.current_token.type == TOKEN_TYPE.NUMBER:
            value = self.current_token.value
        elif self.current_token.type == TOKEN_TYPE.STRING:
            value = self.current_token.value
        elif self.current_token.type == TOKEN_TYPE.TRUE:
            value = True
        elif self.current_token.type == TOKEN_TYPE.FALSE:
            value = False
        elif self.current_token.type == TOKEN_TYPE.NIL:
            value = None
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
        
        self.consume(self.current_token.type)
        return Literal(value)

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, but got {self.current_token.type}")

def parse(file_contents):
    lexer = Lexer(file_contents)
    parser = Parser(lexer)
    
    try:
        expr = parser.parse()
        print(str(expr))
    except SyntaxError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(65)

def tokenize(file_contents):
    lexer = Lexer(file_contents)
    had_error = False
    
    while True:
        token = lexer.next_token()
        if token.type == TOKEN_TYPE.NONE:
            had_error = True
            continue  # Skip printing NONE tokens
        print(token)  # This will use the __str__ method of the Token class
        if token.type == TOKEN_TYPE.EOF:
            break
        if lexer.had_error:
            had_error = True
    
    # Ensure EOF is printed even if we encountered an error
    if token.type != TOKEN_TYPE.EOF:
        print(Token(TOKEN_TYPE.EOF, "", "null"))
    
    return 65 if had_error else 0

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(65)
    
    command = sys.argv[1]
    filename = sys.argv[2]
    
    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(65)
    
    if command == "parse":
        exit(parse(file_contents))
    elif command == "tokenize":
        exit(tokenize(file_contents))

    print("Invalid command.", file=sys.stderr)
    exit(65)

if __name__ == "__main__":
    main()