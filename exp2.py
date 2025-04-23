import os

mnt = []  # Macro Name Table: [index, name, mdt_index]
ala = []  # Argument List Array: [index, name]
mdt = []  # Macro Definition Table

mntc = 0
mdtc = 0
alac = 0


def pass1():
    global mntc, mdtc, alac
    try:
        with open("input.txt") as inp, open("pass1_output.txt", "w") as output:
            lines = inp.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.upper() == "MACRO":
                    i += 1
                    header = lines[i].strip()
                    name_args = header.split()
                    name = name_args[0]
                    args = name_args[1].split(',') if len(name_args) > 1 else []
                    
                    mnt.append([str(mntc + 1), name, str(mdtc)])
                    mntc += 1

                    for arg in args:
                        if '=' in arg:
                            ala.append([str(alac), arg.split('=')[0]])
                        else:
                            ala.append([str(alac), arg])
                        alac += 1

                    i += 1
                    while lines[i].strip().upper() != "MEND":
                        body_line = lines[i].strip()
                        for j in range(alac):
                            if ala[j][1] in body_line:
                                body_line = body_line.replace(ala[j][1], f"#{ala[j][0]}")
                        mdt.append([body_line])
                        mdtc += 1
                        i += 1
                    mdt.append(["MEND"])
                    mdtc += 1
                else:
                    output.write(line + "\n")
                i += 1
    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print(f"Error: {e}")


def pass2():
    alap = 0
    try:
        with open("pass1_output.txt") as inp, open("pass2_output.txt", "w") as output:
            for line in inp:
                line = line.strip()
                tokens = line.split()
                if not tokens:
                    continue
                macro_found = False
                for m in mnt:
                    if tokens[0] == m[1]:
                        args = tokens[1].split(',') if len(tokens) > 1 else []
                        for i, arg in enumerate(args):
                            ala[alap + i][1] = arg
                        mdt_index = int(m[2])
                        i = mdt_index
                        while mdt[i][0].upper() != "MEND":
                            temp = mdt[i][0]
                            if "#" in temp:
                                index = int(temp[temp.index("#") + 1])
                                temp = temp[:temp.index("#")] + ala[alap + index][1]
                            output.write(temp + "\n")
                            i += 1
                        macro_found = True
                        break
                if not macro_found:
                    output.write(line + "\n")
    except FileNotFoundError:
        print("Pass1 output file not found.")
    except Exception as e:
        print(f"Error: {e}")


def display(table, count, cols):
    for i in range(count):
        print(" ".join(table[i][:cols]))


if __name__ == "__main__":
    pass1()
    print("\nMacro Name Table (MNT):")
    display(mnt, mntc, 3)
    print("\nArgument List Array (ALA) after Pass1:")
    display(ala, alac, 2)
    print("\nMacro Definition Table (MDT):")
    display(mdt, mdtc, 1)

    pass2()
    print("\nArgument List Array (ALA) after Pass2:")
    display(ala, alac, 2)
    print("\nNote: Intermediate output of Pass1 and expanded output of Pass2 are stored in files.")
