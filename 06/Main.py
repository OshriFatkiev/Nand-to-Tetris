import Parser
import Code
import SymbolTable

import os
import sys


INIT_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}


def merge(dict1, dict2):
    """ Merges between 2 dictionaries """
    res = {**dict1, **dict2}
    return res


def first_pass(directory_filename):
    """ The first pass of the program. Fill the symbol-table """
    table = SymbolTable.SymbolTable()
    table.d = merge(table.d, INIT_SYMBOLS)
    parser = Parser.Parser(directory_filename)
    index = 0
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            table.add_entry(parser.symbol()[1:-1:], index)  # [1:-1:] to get rid from the parentheses
        else:
            index += 1
        parser.advance()
    return table


def c_command(parser):
    """ C command handler. Converts C commands from assembly to binary """
    dest_m = parser.dest()
    dest_b = Code.dest(dest_m)
    jump_m = parser.jump()
    jump_b = Code.jump(jump_m)
    comp_m = parser.comp()
    if "<<" in comp_m or ">>" in comp_m:
        three_bits = "101"
    else:
        three_bits = "111"
    comp_b = Code.comp(comp_m)
    binary = three_bits + comp_b + dest_b + jump_b
    return binary


def a_command(parser, ram, table):
    """ A command handler. Converts A commands from assembly to binary """
    symbol = parser.symbol().strip("@")
    if not symbol.isnumeric():
        if not table.contains(symbol):
            table.add_entry(symbol, ram)
            address = ram
            ram += 1
        else:
            address = table.get_address(symbol)
    else:
        address = symbol
    binary = bin(int(address))[2:].zfill(16)
    return binary, ram


def second_pass(table, filename):
    """ The second pass. Creates the .hack file """
    ram_available = 16
    name = filename.replace("asm", "hack")
    hack = open(name, 'w')
    parser = Parser.Parser(filename)
    while parser.has_more_commands():
        if parser.command_type() == "C_COMMAND":
            binary = c_command(parser)
            hack.write(binary + '\n')
        elif parser.command_type() == "A_COMMAND":
            binary, ram_available = a_command(parser, ram_available, table)
            hack.write(binary + '\n')
        parser.advance()
    hack.close()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()

    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)

    if directory.endswith(".asm"):    # in case the dir is to specific .asm file
        table = first_pass(directory)
        second_pass(table, directory)
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".asm"):
                file = os.path.join(directory, filename)
                table = first_pass(file)
                second_pass(table, file)
