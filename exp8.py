#Write a program to implement any code optimization techniques
import re

class Op:
    def __init__(self, l, r):
        self.l = l  # Left-hand side (variable)
        self.r = r  # Right-hand side (expression as string)
        self.r_tokens = self._tokenize(r)  # Tokenized right-hand side for comparison

    def _tokenize(self, r):
        """Tokenize the right-hand side into operands and operators."""
        return re.findall(r'[a-zA-Z0-9]+|[+\-*/]', r.replace(" ", ""))

    def __str__(self):
        return f"{self.l} = {self.r}"

# Function for Dead Code Elimination
def dead_code_elimination(op_list):
    """
    Remove operations whose results (left-hand side) are not used in subsequent operations
    or are not part of the final output.
    """
    if not op_list:
        return []

    # Track variables that are used (appear in right-hand sides or are output)
    used_vars = set()
    for op in op_list:
        for token in op.r_tokens:
            if re.match(r'[a-zA-Z0-9]+', token):  # Add operands to used variables
                used_vars.add(token)

    # Keep operations whose left-hand side is used or is the final output
    pr = []
    for i, op in enumerate(op_list):
        # Keep the operation if its result is used or it's the last operation (assumed output)
        if op.l in used_vars or i == len(op_list) - 1:
            pr.append(Op(op.l, op.r))
    
    return pr

# Function for Common Subexpression Elimination
def common_subexpression_elimination(op_list):
    """
    Eliminate common subexpressions by replacing repeated right-hand sides with
    the temporary variable from the first occurrence.
    """
    if not op_list:
        return []

    pr = op_list.copy()  # Create a copy to avoid modifying the input
    for i in range(len(pr)):
        for j in range(i + 1, len(pr)):
            # Check if right-hand sides are identical (same tokens in same order)
            if pr[i].r_tokens == pr[j].r_tokens:
                # Replace all occurrences of pr[j].l with pr[i].l in subsequent right-hand sides
                old_var = pr[j].l
                new_var = pr[i].l
                for k in range(j + 1, len(pr)):
                    # Replace old_var with new_var in tokenized right-hand side
                    new_tokens = [new_var if token == old_var else token for token in pr[k].r_tokens]
                    pr[k].r = " ".join(new_tokens)  # Reconstruct the expression
                    pr[k].r_tokens = new_tokens
                # Mark pr[j] as eliminated by setting its left-hand side to empty
                pr[j].l = ""
    
    # Filter out eliminated operations (those with empty left-hand side)
    return [op for op in pr if op.l]

# Input: List of operations
def input_operations(n):
    op_list = []
    for i in range(n):
        l = input(f"LEFT (variable name for operation {i+1}): ").strip()
        r = input(f"RIGHT (expression for operation {i+1}): ").strip()
        # Validate inputs
        if not re.match(r'[a-zA-Z0-9]+$', l):
            raise ValueError(f"Invalid variable name: {l}")
        if not r or not re.match(r'[a-zA-Z0-9+\-*/ ]+$', r):
            raise ValueError(f"Invalid expression: {r}")
        op_list.append(Op(l, r))
    return op_list

# Print the Intermediate Code
def print_intermediate_code(op_list):
    print("\nINTERMEDIATE CODE:")
    if not op_list:
        print("No operations.")
        return
    for op in op_list:
        print(op)

# Print the optimized code
def print_optimized_code(pr):
    print("\nAFTER DEAD CODE ELIMINATION:")
    if not pr:
        print("No operations remain.")
    else:
        for op in pr:
            print(op)
    
    # Perform common subexpression elimination
    pr = common_subexpression_elimination(pr)
    
    print("\nAFTER COMMON SUBEXPRESSION ELIMINATION:")
    if not pr:
        print("No operations remain.")
    else:
        for op in pr:
            print(op)
    
    print("\nOPTIMIZED CODE:")
    if not pr:
        print("No operations remain.")
    else:
        for op in pr:
            print(op)

def main():
    try:
        n = int(input("ENTER THE NUMBER OF VALUES: "))
        if n < 0:
            raise ValueError("Number of operations cannot be negative")
        
        op_list = input_operations(n)
        
        print_intermediate_code(op_list)
        
        # Perform dead code elimination
        pr = dead_code_elimination(op_list)
        
        # Print optimized code (includes common subexpression elimination)
        print_optimized_code(pr)
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 
