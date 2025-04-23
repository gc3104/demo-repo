#
class IntermediateCode:
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return f"{self.code}"

def generate_intermediate_code(expression):
    """
    Given an expression with n operands and operators, generate intermediate code.
    Example: T = A + B * C - D
    """
    # Validate the expression
    if '=' not in expression:
        raise ValueError("Expression must contain an assignment operator (=)")
    
    # Split into left-hand side (result) and right-hand side (expression)
    try:
        result_var, expr = [s.strip() for s in expression.split('=')]
        if not result_var or not expr:
            raise ValueError("Invalid expression format")
    except ValueError:
        raise ValueError("Invalid expression format")

    # Tokenize the expression into operands and operators
    # Match identifiers (operands), operators (+, -, *, /), and ignore spaces
    tokens = re.findall(r'[a-zA-Z0-9]+|[+\-*/]', expr.replace(" ", ""))
    if not tokens:
        raise ValueError("Expression is empty or invalid")

    # Initialize variables for temporary variables
    temp_count = 1
    intermediate_codes = []

    # Define operator precedence (Higher number = higher precedence)
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    # Stack-based processing for operator precedence
    def process_operator(operators, operands):
        nonlocal temp_count
        if len(operands) < 2 or not operators:
            raise ValueError("Invalid expression: insufficient operands or operators")
        right = operands.pop()
        left = operands.pop()
        operator = operators.pop()
        temp = f"t{temp_count}"
        temp_count += 1
        intermediate_codes.append(IntermediateCode(f"{temp} = {left} {operator} {right}"))
        operands.append(temp)

    # Lists to store operators and operands
    operators = []
    operands = []

    # Process tokens
    for token in tokens:
        if re.match(r'[a-zA-Z0-9]+', token):  # Operand
            operands.append(token)
        elif token in precedence:  # Operator
            while (operators and precedence.get(operators[-1], 0) >= precedence.get(token, 0)):
                process_operator(operators, operands)
            operators.append(token)
        else:
            raise ValueError(f"Invalid token in expression: {token}")

    # Process remaining operators
    while operators:
        process_operator(operators, operands)

    # Final assignment
    if not operands:
        raise ValueError("Invalid expression: no final operand")
    intermediate_codes.append(IntermediateCode(f"{result_var} = {operands[-1]}"))

    return intermediate_codes

# Function to generate intermediate code for a list of expressions
def generate_all_intermediate_code(expressions):
    intermediate_codes = []
    for expression in expressions:
        try:
            intermediate_codes += generate_intermediate_code(expression)
        except ValueError as e:
            print(f"Error processing expression '{expression}': {e}")
    return intermediate_codes

# Driver code
def main():
    # Sample list of expressions
    expressions = [
        "T = A + B * C - D",
        "X = E + F * G * H + I",
        "Y = M - N + O * P",
        "Z = A + B",  # Simple case
        "Result = Var1 + Var2 * Var3"  # Multi-character operands
    ]
    
    # Generate intermediate code
    print("Intermediate Code Generation Output:")
    intermediate_codes = generate_all_intermediate_code(expressions)
    for ic in intermediate_codes:
        print(ic)

if __name__ == "__main__":
    main()
