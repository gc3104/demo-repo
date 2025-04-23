#implementation of lex analyzer for a language whose grammer is known
import re

# Check for delimiter
def is_delimiter(ch):
    return ch in ' +-*/;,<>=()[]{}'

# Check for operator
def is_operator(ch):
    return ch in '+-*/><='

# Check for keyword
def is_keyword(word):
    keywords = {
        "if", "else", "while", "do", "break", "continue", "int", "double", "float",
        "return", "char", "case", "sizeof", "long", "short", "typedef",
        "switch", "unsigned", "void", "static", "struct", "goto"
    }
    return word in keywords

# Check for valid identifier
def is_valid_identifier(word):
    return word and not word[0].isdigit() and not is_delimiter(word[0])

# Check if it's an integer
def is_integer(word):
    return re.fullmatch(r'-?\d+', word) is not None

# Check if it's a real number
def is_real_number(word):
    return re.fullmatch(r'-?\d+\.\d+', word) is not None

# Parsing function
def parse(string):
    tokens = []
    i = 0
    while i < len(string):
        if is_delimiter(string[i]):
            if is_operator(string[i]):
                tokens.append((string[i], "OPERATOR"))
            i += 1
            continue

        j = i
        while j < len(string) and not is_delimiter(string[j]):
            j += 1
        substr = string[i:j]

        if is_keyword(substr):
            tokens.append((substr, "KEYWORD"))
        elif is_integer(substr):
            tokens.append((substr, "INTEGER"))
        elif is_real_number(substr):
            tokens.append((substr, "REAL NUMBER"))
        elif is_valid_identifier(substr):
            tokens.append((substr, "VALID IDENTIFIER"))
        else:
            tokens.append((substr, "INVALID IDENTIFIER"))
        i = j

    for token, token_type in tokens:
        print(f"'{token}' IS A {token_type}")

# Example
code = "int a = b + 1c;"
parse(code)
