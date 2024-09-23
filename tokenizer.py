import sys

def handle_string(file_contents, start_index, line_number):
    i = start_index + 1  # Start after the opening quote
    length = len(file_contents)
    string_literal = ""
    
    while i < length:
        c = file_contents[i]
        if c == '"':
            # Found closing quote
            lexeme = file_contents[start_index:i+1]
            return lexeme, string_literal, line_number, i, False
        elif c == '\n':
            line_number += 1
        
        string_literal += c
        i += 1
    
    # If we've reached here, the string is unterminated
    print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
    return "", "", line_number, i, True

def handle_number(file_contents, start_index):
    i = start_index
    length = len(file_contents)
    
    while i < length and file_contents[i].isdigit():
        i += 1
    
    if i < length and file_contents[i] == '.':
        i += 1
        while i < length and file_contents[i].isdigit():
            i += 1
    
    lexeme = file_contents[start_index:i]
    literal = float(lexeme)
    return lexeme, literal, i

def handle_identifier(file_contents, start_index):
    reserved_words = {
        "and": "AND",
        "class": "CLASS",
        "else": "ELSE",
        "false": "FALSE",
        "for": "FOR",
        "fun": "FUN",
        "if": "IF",
        "nil": "NIL",
        "or": "OR",
        "print": "PRINT",
        "return": "RETURN",
        "super": "SUPER",
        "this": "THIS",
        "true": "TRUE",
        "var": "VAR",
        "while": "WHILE"
    }
    
    i = start_index
    length = len(file_contents)
    
    while i < length and (file_contents[i].isalnum() or file_contents[i] == '_'):
        i += 1
    
    lexeme = file_contents[start_index:i]
    
    if lexeme in reserved_words:
        return reserved_words[lexeme], lexeme, i
    else:
        return "IDENTIFIER", lexeme, i

def main():
    print("Logs from your program will appear here!", file=sys.stderr)
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
    
    command = sys.argv[1]
    filename = sys.argv[2]
    
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    
    with open(filename) as file:
        file_contents = file.read()
    
    line_number = 1
    error_occurred = False
    i = 0
    length = len(file_contents)
    
    while i < length:
        c = file_contents[i]
        if c in " \t":
            i += 1
            continue
        elif c == "\n":
            line_number += 1
            i += 1
            continue
        elif c == "{":
            print("LEFT_BRACE { null")
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == "(":
            print("LEFT_PAREN ( null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "*":
            print("STAR * null")
        elif c == ".":
            print("DOT . null")
        elif c == ",":
            print("COMMA , null")
        elif c == "+":
            print("PLUS + null")
        elif c == "-":
            print("MINUS - null")
        elif c == "=":
            if i + 1 < length and file_contents[i + 1] == "=":
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif c == "!":
            if i + 1 < length and file_contents[i + 1] == "=":
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif c == "<":
            if i + 1 < length and file_contents[i + 1] == "=":
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif c == ">":
            if i + 1 < length and file_contents[i + 1] == "=":
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif c == "/":
            if i + 1 < length and file_contents[i + 1] == "/":
                while i < length and file_contents[i] != "\n":
                    i += 1
                continue
            else:
                print("SLASH / null")
        elif c == ";":
            print("SEMICOLON ; null")
        elif c == ":":
            print("COLON : null")
        elif c == '"':
            lexeme, string_literal, line_number, i, error_occurred = handle_string(file_contents, i, line_number)
            if not error_occurred:
                print(f"STRING {lexeme} {string_literal}")
            else:
                break
        elif c.isdigit():
            lexeme, number_literal, i = handle_number(file_contents, i)
            print(f"NUMBER {lexeme} {number_literal}")
            continue
        elif c.isalpha() or c == '_':
            token_type, lexeme, i = handle_identifier(file_contents, i)
            print(f"{token_type} {lexeme} null")
            continue
        else:
            print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
            error_occurred = True
        
        i += 1
    
    print("EOF null")
    
    if error_occurred:
        exit(65)

if __name__ == "__main__":
    main()
