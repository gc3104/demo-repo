#implementation of recursive descent parser
print("Recursive Descent Parsing For following grammar\n")
print("E -> TE'\nE' -> +TE' | ε\nT -> FT'\nT' -> *FT' | ε\nF -> (E) | i\n")

print("Enter the string you want to be checked")

# Input string to be parsed
s = list(input())

# Initialize index for the input string
i = 0

# Match function to check if the current character matches 'a'
def match(a):
    global s
    global i
    if i >= len(s):
        return False
    elif s[i] == a:
        i += 1
        return True
    else:
        return False

# F -> (E) | i
def F():
    if match("("):  # Check for open parentheses
        if E():  # Parse expression E
            if match(")"):  # Match closing parentheses
                return True
            else:
                return False
        else:
            return False
    elif match("i"):  # Check for terminal 'i'
        return True
    else:
        return False

# T' -> *FT' | ε
def Tx():
    if match("*"):  # Check for multiplication symbol
        if F():  # Match F
            if Tx():  # Recursive call for T'
                return True
            else:
                return False
    else:
        return True  # If no multiplication, return True (ε)

# T -> FT'
def T():
    if F():  # Match F
        if Tx():  # Match T'
            return True
    return False

# E' -> +TE' | ε
def Ex():
    if match("+"):  # Match '+'
        if T():  # Match T
            if Ex():  # Recursive call for E'
                return True
            else:
                return False
    else:
        return True  # If no '+', return True (ε)

# E -> TE'
def E():
    if T():  # Match T
        if Ex():  # Match E'
            return True
    return False

# Start parsing the input string
if E():  # Start parsing with E
    if i == len(s):  # Check if all characters are consumed
        print("String is accepted")
    else:
        print("String is not accepted")
else:
    print("String is not accepted")

 
# Grammar:
# e -> t b
# b -> + t b | ε
# t -> f c
# c -> * f c | ( e ) | ε
# f -> i

# Non-terminals: e, b, t, c, f
# Terminals: i, +, *, (, ), $

# Predictive Parsing Table (with full production strings)
m = [
    ["t b", "", "", "t b", "", ""],        # e
    ["", "+ t b", "", "", "ε", "ε"],       # b
    ["f c", "", "* f c", "", "", ""],      # t
    ["", "ε", "* f c", "( e )", "ε", "ε"], # c <-- FIXED: Added "ε" for '+' in c-row
    ["i", "", "", "", "", ""]              # f
]


# Maps for table lookup
non_terminal_map = {'e': 0, 'b': 1, 't': 2, 'c': 3, 'f': 4}
terminal_map = {'i': 0, '+': 1, '*': 2, '(': 3, ')': 4, '$': 5}

# Stack operations
def push(stack, symbols):
    for symbol in symbols:
        stack.append(symbol)
    return len(stack) - 1

def pop(stack, stack_top, count=1):
    for _ in range(count):
        if stack_top >= 0:
            stack.pop()
            stack_top -= 1
    return stack_top

# Input validation
def is_valid_input(input_string):
    valid_terminals = {'i', '+', '*', '(', ')'}
    return all(c in valid_terminals for c in input_string)

# Main parser function
def parse(input_string):
    if not is_valid_input(input_string):
        print("\nERROR: Input contains invalid characters")
        return

    input_string += "$"
    stack = ['$', 'e']
    stack_top = 1
    input_pos = 0

    print("\nStack\t\tInput")
    print("___________________________")

    while stack[stack_top] != '$' or input_string[input_pos] != '$':
        print(" ".join(stack[:stack_top+1]), "\t\t", input_string[input_pos:])

        top = stack[stack_top]
        current_input = input_string[input_pos]

        # Terminal at top
        if top in terminal_map:
            if top == current_input:
                stack_top = pop(stack, stack_top, 1)
                input_pos += 1
            else:
                print("\nERROR: Terminal mismatch")
                return

        # Non-terminal at top
        elif top in non_terminal_map:
            nt_index = non_terminal_map[top]
            t_index = terminal_map.get(current_input, -1)

            if t_index == -1 or m[nt_index][t_index] == "":
                print("\nERROR: Invalid production")
                return

            production = m[nt_index][t_index]
            stack_top = pop(stack, stack_top, 1)

            if production != "ε":
                symbols = list(reversed(production.split()))
                stack_top = push(stack, symbols)
        else:
            print("\nERROR: Unknown symbol on stack")
            return

    # Final state
    print(" ".join(stack[:stack_top+1]), "\t\t", input_string[input_pos:])
    print("\nSUCCESS")
# Main execution
if __name__ == "__main__":
    input_string = input("Enter the input string: ")
    parse(input_string)


