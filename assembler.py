
import re
import os


symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    symbol_table[f"R{i}"] = i




dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp_table = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

jump_table = {
    "null": "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111"
}



def read_file(filename):
    cleaned_lines = []

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.split("//")[0].strip()

            if line:
                cleaned_lines.append((line, line_number))

    return cleaned_lines



def first_pass(instructions):
    labels = {}
    instruction_address = 0

    for instruction, line_number in instructions:

        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]

            if not re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", label):
                print(f"Warning: Invalid label at line {line_number}: {instruction}")
                continue

            if label in labels or label in symbol_table:
                print(f"Warning: Duplicate label '{label}' at line {line_number}")
                continue

            labels[label] = instruction_address

        else:
            instruction_address += 1

    return labels




def parse_c_instruction(instruction):
    dest = "null"
    comp = ""
    jump = "null"

    if ";" in instruction:
        comp_jump = instruction.split(";")

        if len(comp_jump) != 2:
            raise ValueError("Invalid jump format")

        comp, jump = comp_jump

    else:
        comp = instruction

    if "=" in comp:
        parts = comp.split("=")

        if len(parts) != 2:
            raise ValueError("Invalid destination format")

        dest, comp = parts

    return dest.strip(), comp.strip(), jump.strip()



def convert_c_instruction(instruction):
    dest, comp, jump = parse_c_instruction(instruction)

    if comp not in comp_table:
        raise ValueError(f"Invalid comp field: {comp}")

    if dest not in dest_table:
        raise ValueError(f"Invalid dest field: {dest}")

    if jump not in jump_table:
        raise ValueError(f"Invalid jump field: {jump}")

    binary = (
        "111"
        + comp_table[comp]
        + dest_table[dest]
        + jump_table[jump]
    )

    return binary




def second_pass(instructions, labels):
    binary_lines = []
    variables = {}
    next_variable_address = 16

    # Combine predefined symbols and labels
    current_symbols = symbol_table.copy()
    current_symbols.update(labels)

    for instruction, line_number in instructions:

        # Skip labels
        if instruction.startswith("(") and instruction.endswith(")"):
            continue

        try:

            # A-INSTRUCTION
            if instruction.startswith("@"):
                symbol = instruction[1:].strip()

                if not symbol:
                    raise ValueError("Empty A-instruction")

                if symbol.isdigit():
                    address = int(symbol)

                    if not 0 <= address <= 32767:
                        raise ValueError("Address must be between 0 and 32767")

                else:
                    if not re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", symbol):
                        raise ValueError(f"Invalid symbol: {symbol}")

                    if symbol not in current_symbols:
                        current_symbols[symbol] = next_variable_address
                        variables[symbol] = next_variable_address
                        next_variable_address += 1

                    address = current_symbols[symbol]

                binary = format(address, "016b")

            # C-INSTRUCTION
            else:
                binary = convert_c_instruction(instruction)

            binary_lines.append(binary)

        except (ValueError, KeyError) as error:
            print(f"Error at line {line_number}: {instruction}")
            print(f"Reason: {error}")

    return binary_lines, variables, current_symbols



def save_symbols(labels, variables):
    with open("symbols.txt", "w") as file:

        file.write("LABELS\n")
        file.write("====================\n")

        for name, address in labels.items():
            file.write(f"{name} = {address}\n")

        file.write("\nVARIABLES\n")
        file.write("====================\n")

        for name, address in variables.items():
            file.write(f"{name} = {address}\n")



def assemble(filename):

    global symbol_table

    symbol_table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }

    for i in range(16):
        symbol_table[f"R{i}"] = i

    instructions = read_file(filename)

    labels = first_pass(instructions)

    binary_lines, variables, all_symbols = second_pass(
        instructions, labels
    )

    output_filename = os.path.splitext(filename)[0] + ".hack"

    with open(output_filename, "w") as file:
        file.write("\n".join(binary_lines))

        if binary_lines:
            file.write("\n")

    save_symbols(labels, variables)

    print("\nAssembly completed!")
    print(f"Output file: {output_filename}")
    print(f"Symbols file: symbols.txt")




if __name__ == "__main__":

    filename = input("Enter assembly file name: ").strip()

    try:
        assemble(filename)

    except FileNotFoundError:
        print("Error: File not found.")

    except Exception as error:
        print(f"Unexpected error: {error}")
