from CodeWriter import *
from Parser import *

import os
import sys


def main(directory, name):
    """ The main function of the VMtranslator """

    parser = Parser(directory)
    code = CodeWriter(name)
    current_vm_file = os.path.basename(directory).strip(".vm")
    command_handler(parser, code, current_vm_file)
    code.close()


def command_handler(parser, code, current_vm_file):
    """ Handles the translation of each command from the .vm file """

    current_function = ""

    while parser.has_more_commands():
        cmd = parser.command_type()

        if cmd in ["C_IF", "C_LABEL", "C_GOTO", "C_ARITHMETIC"]:
            arg = parser.arg1()
            if cmd == "C_ARITHMETIC":
                code.write_arithmetic(arg, parser, current_function)
            elif cmd == "C_IF" and current_function is not None:
                code.write_if(current_function + "$" + arg)
            elif cmd == "C_GOTO" and current_function is not None:
                code.write_goto(current_function + "$" + arg)
            elif cmd == "C_LABEL" and current_function is not None:
                code.write_label(current_function + "$" + arg)

        elif cmd in ["C_PUSH", "C_POP"]:
            seg = parser.arg1()
            ind = parser.arg2()
            code.write_push_pop(cmd, seg, ind, current_vm_file)

        elif cmd == "C_FUNCTION":
            function_name = parser.arg1()
            n_args = parser.arg2()
            current_function = function_name
            code.write_function(function_name, n_args)

        elif cmd == "C_CALL":
            function_name = parser.arg1()
            n_args = parser.arg2()
            code.write_call(function_name, n_args, parser.line_num)

        elif cmd == "C_RETURN":
            code.write_return()

        parser.advance()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()

    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)

    if not os.path.isfile(directory):
        directory = os.path.abspath(directory)

    if directory.endswith(".vm"):  # in case the dir is to specific .vm file
        name = directory.replace("vm", "asm")
        main(directory, name)

    else:                          # in case the dir is to some folder
        name = os.path.basename(directory) + ".asm"
        for filename in os.listdir(directory):
            if filename.endswith(".vm"):
                file = os.path.join(directory, filename)
                name = os.path.join(directory, name)
                main(file, name)


