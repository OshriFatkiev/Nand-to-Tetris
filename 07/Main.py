from CodeWriter import *
from Parser import *

import os
import sys


def main(directory, name):
    """ The main function of the VMtranslator """

    parser = Parser(directory)
    code = CodeWriter(name)

    while parser.has_more_commands():
        cmd = parser.command_type()

        if cmd == "C_ARITHMETIC":
            operator = parser.arg1()
            code.write_arithmetic(operator)

        elif cmd in ["C_PUSH", "C_POP"]:
            seg = parser.arg1()
            ind = parser.arg2()
            code.write_push_pop(cmd, seg, ind)
        parser.advance()

    code.close()


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


