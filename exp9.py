# Write a program to generate target code
def generate_target_code(expression):
    # Parse the expression (T = A OP B)
    parts = expression.split('=')
    left_side = parts[0].strip()  # Left part (T)
    right_side = parts[1].strip()  # Right part (A OP B)
    
    # Extract operands and operator from the right side
    operand_A, operator, operand_B = right_side.split()
    
    # Generate MOV instructions to load operands into registers
    print(f"MOV {operand_A}, R1")  # Move A into R1
    print(f"MOV {operand_B}, R2")  # Move B into R2
    
    # Generate the appropriate arithmetic operation based on the operator
    if operator == "+":
        print("ADD R1, R2")  # Add R2 to R1
    elif operator == "-":
        print("SUB R1, R2")  # Subtract R2 from R1
    elif operator == "*":
        print("MUL R1, R2")  # Multiply R1 by R2
    elif operator == "/":
        print("DIV R1, R2")  # Divide R1 by R2
    else:
        print("ERROR: Invalid operator!")
        return
    
    # Move the result into the left side variable (T)
    print(f"MOV R1, {left_side}")  # Store the result in T

def main():
    # Input the expression (T = A OP B)
    expression = input("Enter an expression (T = A OP B): ")
    
    print("\nGenerated Target Code:")
    generate_target_code(expression)

if __name__ == "__main__":
    main()
