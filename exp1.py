#Implementation of two pass assembler
import sys

def RemoveSpaces(x):
    """Filter out empty strings, spaces, and comma-separated spaces."""
    return x.strip() != "" and x.strip() != "," and x.strip() != "\t"

def RemoveCommas(x):
    """Remove trailing commas, whitespace, and colons from a string."""
    return x.rstrip(", \t:")

def CheckLiteral(element):
    """Check if an element is a literal (starts with =' and ends with ')."""
    return element.startswith("='") and element.endswith("'")

def CheckSymbol(Elements):
    """Check if the last element is a variable (not a register, literal, opcode, or label)."""
    global SymbolTable, Opcodes
    last = Elements[-1]
    if (len(Elements) > 1 and 
        Elements[0] not in ["BRZ", "BRN", "BRP"] and 
        (len(Elements) < 2 or Elements[1] not in ["BRZ", "BRN", "BRP"]) and
        last not in Opcodes and 
        last[:2] != "='" and 
        last[:3] != "REG" and 
        not last.isnumeric() and 
        last not in [x[0] for x in SymbolTable]):
        return True
    return False

def CheckLabel(Elements):
    """Check if the first element is a label (followed by an opcode)."""
    global SymbolTable, Opcodes
    label = Elements[0].rstrip(":")  # Remove colon from label
    if (len(Elements) >= 2 and 
        Elements[1] in Opcodes and 
        label not in [x[0] for x in SymbolTable]):
        return True
    return False

Opcodes = ["CLA", "LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV", "STP", "DATA", "START", "END"]
AssemblyOpcodes = {
    "CLA": "0000", "LAC": "0001", "SAC": "0010", "ADD": "0011", "SUB": "0100",
    "BRZ": "0101", "BRN": "0110", "BRP": "0111", "INP": "1000", "DSP": "1001",
    "MUL": "1010", "DIV": "1011", "STP": "1100"
}
Registers = {
    "REG1": 0,
    "REG2": 1,
    "REG3": 2,
    "REG4": 3
}
SymbolTable = []
LiteralTable = []
Variables = []
Declarations = []
AssemblyCode = []
location_counter = 0
end_found = False
line_number = 0

# Open input file
try:
    file = open("Assembly Code Input.txt", "rt")
except FileNotFoundError:
    print("FileError: 'Assembly Code Input.txt' not found.")
    sys.exit(0)

# ERROR 1: Check for missing START statement
lines = file.readlines()
file.seek(0)
for line in lines:
    if line[:2] != "//" and line.strip():
        if line.strip().split()[0] != "START":
            print(f"STARTError: 'START' statement is missing. (Line {line_number})")
            file.close()
            sys.exit(0)
        break
    line_number += 1

# First Pass
line_number = 0
for line in lines:
    line_number += 1
    if line[:2] == "//" or not line.strip():
        continue
    Elements = line.strip().split()
    Elements = list(filter(RemoveSpaces, Elements))
    Elements = list(map(RemoveCommas, Elements))

    # Remove inline comments
    for i in range(len(Elements)):
        if Elements[i][:2] == "//":
            Elements = Elements[:i]
            break

    if not Elements:
        continue

    # ERROR 2: Check for too many operands
    if len(Elements) >= 3 and Elements[0] in Opcodes and Elements[0] not in ["START", "DATA"]:
        print(f"TooManyOperandsError: Too many operands for '{Elements[0]}'. (Line {line_number})")
        file.close()
        sys.exit(0)
    if len(Elements) >= 4 and Elements[1] in Opcodes:
        print(f"TooManyOperandsError: Too many operands for '{Elements[1]}'. (Line {line_number})")
        file.close()
        sys.exit(0)

    # ERROR 3: Check for less operands
    if len(Elements) == 1 and Elements[0] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]:
        print(f"LessOperandsError: Less operands for '{Elements[0]}'. (Line {line_number})")
        file.close()
        sys.exit(0)
    if len(Elements) == 2 and Elements[1] in ["LAC", "SAC", "ADD", "SUB", "BRZ", "BRN", "BRP", "INP", "DSP", "MUL", "DIV"]:
        print(f"LessOperandsError: Less operands for '{Elements[1]}'. (Line {line_number})")
        file.close()
        sys.exit(0)

    # ERROR 4: Check for invalid opcodes
    if len(Elements) == 3 and Elements[1] not in Opcodes:
        print(f"InvalidOpcodeError: '{Elements[1]}' is invalid. (Line {line_number})")
        file.close()
        sys.exit(0)
    if len(Elements) == 2 and Elements[0] not in Opcodes and Elements[1] != "CLA":
        print(f"InvalidOpcodeError: '{Elements[0]}' is invalid. (Line {line_number})")
        file.close()
        sys.exit(0)

    # ERROR 5: Check for CLA operands
    if Elements[0] == "CLA" or (len(Elements) >= 2 and Elements[1] == "CLA"):
        if len(Elements) > 2:
            print(f"OperandError: CLA takes no operands. (Line {line_number}, Parsed: {Elements})")
            file.close()
            sys.exit(0)
        if len(Elements) == 2 and Elements[0] == "CLA" and Elements[1] != "":
            print(f"OperandError: CLA takes no operands. (Line {line_number}, Parsed: {Elements})")
            file.close()
            sys.exit(0)

    # Handle START
    if Elements[0] == "START":
        if len(Elements) > 1 and Elements[1].isdigit():
            location_counter = int(Elements[1])
        continue

    # Handle END
    if Elements[0] == "END":
        end_found = True
        continue

    # Handle DATA directives
    if len(Elements) == 3 and Elements[1] == "DATA":
        var_name, value = Elements[0], Elements[2]
        if not value.isdigit():
            print(f"ValueError: DATA value '{value}' must be numeric. (Line {line_number})")
            file.close()
            sys.exit(0)
        if var_name in Variables:
            print(f"DefinationError: Variable '{var_name}' defined multiple times. (Line {line_number})")
            file.close()
            sys.exit(0)
        Variables.append(var_name)
        Declarations.append((var_name, value))
        for i, (sym, addr, val, typ) in enumerate(SymbolTable):
            if sym == var_name and typ == "Variable" and addr is None:
                SymbolTable[i] = [var_name, location_counter, int(value), "Variable"]
                break
        else:
            SymbolTable.append([var_name, location_counter, int(value), "Variable"])
        location_counter += 1
        continue

    # Check for Literals
    for x in Elements:
        if CheckLiteral(x) and x not in [l[0] for l in LiteralTable]:
            LiteralTable.append([x, -1])

    # Check for Labels
    if CheckLabel(Elements):
        label = Elements[0].rstrip(":")  # Remove colon for SymbolTable
        SymbolTable.append([label, location_counter, None, "Label"])

    # Check for Symbols (variables used in instructions)
    if CheckSymbol(Elements):
        SymbolTable.append([Elements[-1], None, None, "Variable"])

    location_counter += 1

# Assign literal addresses
for i in range(len(LiteralTable)):
    if LiteralTable[i][1] == -1:
        LiteralTable[i][1] = location_counter
        location_counter += 1

# ERROR 7: Check for missing END statement
if not end_found:
    print(f"ENDError: 'END' statement is missing. (Line {line_number})")
    file.close()
    sys.exit(0)

# ERROR 8: Check for undefined variables
for x in SymbolTable:
    if x[1] is None and x[3] == "Variable":
        print(f"UndefinedVariableError: Variable '{x[0]}' not defined.")
        file.close()
        sys.exit(0)

# Printing Tables after First Pass
print(">>> Opcode Table <<<\n")
print("ASSEMBLY OPCODE OPCODE")
print("--------------------------")
for key in AssemblyOpcodes:
    print(key.ljust(20) + AssemblyOpcodes[key])
print("--------------------------")

print("\n>>> Literal Table <<<\n")
print("LITERAL ADDRESS")
print("-------------------")
for literal, addr in LiteralTable:
    print(literal.ljust(12) + str(addr))
print("-------------------")

print("\n>>> Symbol Table <<<\n")
print("SYMBOL ADDRESS VALUE TYPE")
print("----------------------------------------------")
for sym, addr, val, typ in SymbolTable:
    print(f"{sym.ljust(16)}{str(addr).ljust(12)}{str(val).ljust(10)}{typ}")
print("----------------------------------------------")

print("\n>>> Data Table <<<\n")
print("VARIABLES VALUE")
print("-------------------")
for var, val in Declarations:
    print(f"{var.ljust(14)}{val}")
print("-------------------\n")

# Second Pass
file.seek(0)
print(">>> MACHINE CODE <<<\n")
location_counter = 1  # Reset for instructions, assuming START 1
line_number = 0
for line in file:
    line_number += 1
    if line[:2] == "//" or not line.strip():
        continue
    Elements = line.strip().split()
    Elements = list(filter(RemoveSpaces, Elements))
    Elements = list(map(RemoveCommas, Elements))

    # Remove inline comments
    for i in range(len(Elements)):
        if Elements[i][:2] == "//":
            Elements = Elements[:i]
            break

    if not Elements:
        continue

    if Elements[0] == "START":
        continue
    if Elements[0] == "END" or (len(Elements) == 3 and Elements[1] == "DATA"):
        break

    s = ""
    addr = location_counter
    opcode = ""
    operand_addr = 0

    # Handle STP
    if Elements[0] == "STP":
        opcode = AssemblyOpcodes["STP"]
        s = f"{addr:02d} {opcode} 00 00 00"
        AssemblyCode.append(s)
        print(s)
        location_counter += 1
        continue

    # Handle CLA
    if Elements[0] == "CLA" or (len(Elements) >= 2 and Elements[1] == "CLA"):
        if len(Elements) > 1 and Elements[1] == "CLA":
            for sym, sym_addr, _, typ in SymbolTable:
                if sym == Elements[0].rstrip(":") and typ == "Label":
                    addr = sym_addr
                    break
        opcode = AssemblyOpcodes["CLA"]
        if len(Elements) > 2:
            print(f"OperandError: CLA takes no operands. (Line {line_number}, Parsed: {Elements})")
            file.close()
            sys.exit(0)
        if len(Elements) == 2 and Elements[0] == "CLA" and Elements[1] != "":
            print(f"OperandError: CLA takes no operands. (Line {line_number}, Parsed: {Elements})")
            file.close()
            sys.exit(0)
        s = f"{addr:02d} {opcode} 00 00 00"
        AssemblyCode.append(s)
        print(s)
        location_counter += 1
        continue

    # Handle instructions with labels
    if len(Elements) == 3 and Elements[1] in Opcodes:
        for sym, sym_addr, _, typ in SymbolTable:
            if sym == Elements[0].rstrip(":") and typ == "Label":
                addr = sym_addr
                break
        opcode = AssemblyOpcodes[Elements[1]]
        operand = Elements[2]
    else:
        opcode = AssemblyOpcodes[Elements[0]]
        operand = Elements[1] if len(Elements) > 1 else ""

    s = f"{addr:02d} {opcode} "

    # Handle operand
    if operand:
        if CheckLiteral(operand):
            for lit, lit_addr in LiteralTable:
                if lit == operand:
                    operand_addr = lit_addr
                    break
            s += f"00 00 {operand_addr:02d}"
        elif operand in [x[0] for x in SymbolTable]:
            for sym, sym_addr, _, typ in SymbolTable:
                if sym == operand and typ in ["Label", "Variable"]:
                    operand_addr = sym_addr
                    break
            if typ == "Label" and (Elements[0] in ["BRZ", "BRN", "BRP"] or (len(Elements) > 1 and Elements[1] in ["BRZ", "BRN", "BRP"])):
                s += f"{operand_addr:02d} 00 00"
            else:
                s += f"00 00 {operand_addr:02d}"
        elif operand[:3] == "REG":
            reg_num = Registers.get(operand, -1)
            if reg_num == -1:
                print(f"InvalidRegisterError: '{operand}' is not a valid register. (Line {line_number})")
                file.close()
                sys.exit(0)
            operand_addr = reg_num
            s += f"00 {operand_addr:02d} 00"
        else:
            print(f"InvalidOperandError: '{operand}' is invalid. (Line {line_number})")
            file.close()
            sys.exit(0)
    else:
        s += "00 00 00"

    AssemblyCode.append(s)
    print(s)
    location_counter += 1

# Write machine code to file
file.close()
try:
    with open("Machine Code.txt", "w") as file:
        file.write("------------\nMACHINE CODE\n------------\n\n")
        for x in AssemblyCode:
            file.write(x + "\n")
except IOError:
    print("FileError: Unable to write to 'Machine Code.txt'.")
    sys.exit(0)
"""START 1
LoopOne: CLA
LAC A
ADD ='1'
SUB ='35'
Loop: BRP Subtraction
Subtraction: SUB ='5'
ADD B
MUL C
SUB D
MUL ='600'
BRZ Zero
Division: DIV E
CLA
LAC REG1
BRP Positive
Zero: SAC X
DSP X
STP
Positive: CLA
DSP REG1
DSP REG2
A DATA 250
B DATA 125
C DATA 90
D DATA 88
E DATA 5
X DATA 0
END"""
