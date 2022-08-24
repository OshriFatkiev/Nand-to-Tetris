import os
import random
import string

ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"


def random_word(length):
    """ Generate random word with the desired length """
    let = string.ascii_lowercase
    return ''.join(random.choice(let) for i in range(length))


class CodeWriter:
    """ Translates VM commands into Hack assembly code """

    def __init__(self, out):
        """ The CodeWriter constructor """
        self.words = []
        self.output = open(out, 'a')

    def get_name(self):
        """ Returns the name of the file """
        return os.path.basename(self.output.name).strip("asm")

    def write_arithmetic(self, cmd):
        """ Converts the arithmetic commands to Assembly """
        lst = []

        if cmd == ADD:
            lst = [
                "// add\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    D=M\n",
                "    M=0\n",
                "    A=A-1\n",
                "    M=M+D\n"
            ]

        elif cmd == SUB:
            lst = [
                "// sub\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M-1\n",
                "    D=M\n",
                "    @SP\n",
                "    A=M\n",
                "    D=D-M\n"
                "    M=0\n",
                "    @SP\n",
                "    A=M-1\n",
                "    M=D\n"
            ]

        elif cmd == NEG:
            lst = [
                "// neg\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    M=-M\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd == AND:
            lst = [
                "// and\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    D=M\n",
                "    M=0\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    D=D&M\n",
                "    @SP\n",
                "    A=M\n",
                "    M=D\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd == OR:
            lst = [
                "// and\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    D=M\n",
                "    M=0\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    D=D|M\n",
                "    @SP\n",
                "    A=M\n",
                "    M=D\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd == NOT:
            lst = [
                "// not\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    M=!M\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd in [EQ, GT, LT]:

            x_sign = random_word(6)         # making sure no label occurs twice
            while x_sign in self.words:
                x_sign = random_word(6)
            self.words.append(x_sign)
            same_sign = random_word(6)
            while same_sign in self.words:
                same_sign = random_word(6)
            self.words.append(same_sign)
            true = random_word(6)
            while true in self.words:
                true = random_word(6)
            self.words.append(true)
            false = random_word(6)
            while false in self.words:
                false = random_word(6)
            self.words.append(false)
            end = random_word(6)
            while end in self.words:
                end = random_word(6)
            self.words.append(end)

            jump, jump_two = '', ''
            if cmd == GT:
                jump = "JGT"
                jump_two = "JLE"
            elif cmd == LT:
                jump = "JLT"
                jump_two = "JGE"

            if cmd == GT or cmd == LT:

                lst = [
                    "// " + cmd + "\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M-1\n",
                    "    D=M\n",                # D = x
                    "    @" + x_sign + "\n",
                    "    D;" + jump + "\n",     # x < 0
                    "    @SP\n",
                    "    A=M\n",
                    "    D=M\n",                # D = y
                    "    @" + false + "\n",
                    "    D;" + jump + "\n",
                    "(" + same_sign + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    D=M\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    D=D-M\n",
                    "    @" + true + "\n",
                    "    D;" + jump + "\n",
                    "    @" + false + "\n",
                    "    0;JMP\n",
                    "(" + x_sign + ")" + "\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    @" + true + "\n",
                    "    D;" + jump_two + "\n",
                    "    @" + same_sign + "\n",
                    "    0;JMP\n",
                    "(" + true + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    M=-1\n",
                    "    @" + end + "\n",
                    "    0;JMP\n",
                    "(" + false + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    M=0\n",
                    "    @" + end + "\n",
                    "    0;JMP\n",
                    "(" + end + ")" + "\n",
                ]

            else:
                jump = "JGE"
                lst = [
                    "// " + cmd + "\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M-1\n",
                    "    D=M\n",
                    "    @" + x_sign + "\n",
                    "    D;" + jump + "\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    @" + false + "\n",
                    "    M;" + jump + "\n",
                    "(" + same_sign + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    D=M\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    D=D-M\n",
                    "    @" + true + "\n",
                    "    D;JEQ\n",
                    "    @" + false + "\n",
                    "    0;JMP\n",
                    "(" + x_sign + ")" + "\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    @" + same_sign + "\n",
                    "    D;" + jump + "\n",
                    "    @" + false + "\n",
                    "    0;JMP\n",
                    "(" + true + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    M=-1\n",
                    "    @" + end + "\n",
                    "    0;JMP\n",
                    "(" + false + ")" + "\n",
                    "    @SP\n",
                    "    A=M-1\n",
                    "    M=0\n",
                    "    @" + end + "\n",
                    "    0;JMP\n",
                    "(" + end + ")" + "\n",
                ]

        self.output.writelines(lst)

    def write_push_pop(self, cmd, seg, ind):
        """ Write push and pop command in Assembly """
        lst = []

        if cmd == "C_PUSH":

            if seg in ["local", "argument", "this", "that"]:
                if seg == "local":
                    seg = "LCL"
                elif seg == "argument":
                    seg = "ARG"
                elif seg == "this":
                    seg = "THIS"
                else:
                    seg = "THAT"

                lst = [
                    "// push " + seg + " " + str(ind) + "\n",
                    "    @" + str(ind) + "\n",
                    "    D=A\n",
                    "    @" + seg + "\n",
                    "    M=M+D\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @SP\n",
                    "    M=M+1\n",
                    "    @" + str(ind) + "\n",
                    "    D=A\n",
                    "    @" + seg + "\n",
                    "    M=M-D\n",
                ]

            elif seg == "constant":
                lst = [
                    "// push constant " + str(ind) + "\n",
                    "    @" + str(ind) + "\n",
                    "    D=A\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @SP\n",
                    "    M=M+1\n"
                ]

            elif seg == "static":
                lst = [
                    "// push static " + str(ind) + "\n",
                    "    @" + self.get_name() + ind + "\n",
                    "    D=M\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @SP\n",
                    "    M=M+1\n"
                ]

            elif seg == "temp":  # RAM 5 to 12
                lst = [
                    "// push temp " + str(ind) + "\n",
                    "    @" + str(int(ind) + 5) + "\n",
                    "    D=M\n"
                    "    @SP\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @SP\n",
                    "    M=M+1\n",
                ]

            elif seg == "pointer" and int(ind) in [0, 1]:
                if int(ind) == 0:    # THIS
                    lst = [
                        "// push pointer 0\n" 
                        "    @THIS\n",
                        "    D=M\n",
                        "    @SP\n",
                        "    A=M\n",
                        "    M=D\n",
                        "    @SP\n",
                        "    M=M+1\n"
                    ]
                else:           # THAT
                    lst = [
                        "// push pointer 1\n"
                        "    @THAT\n",
                        "    D=M\n",
                        "    @SP\n",
                        "    A=M\n",
                        "    M=D\n",
                        "    @SP\n",
                        "    M=M+1\n"
                    ]

        elif cmd == "C_POP":
            if seg in ["local", "argument", "this", "that"]:

                if seg == "local":
                    seg = "LCL"
                elif seg == "argument":
                    seg = "ARG"
                elif seg == "this":
                    seg = "THIS"
                else:
                    seg = "THAT"

                lst = [
                    "// pop " + seg + " " + str(ind) + "\n",
                    "    @" + str(ind) + "\n",
                    "    D=A\n",
                    "    @" + seg + "\n",
                    "    M=M+D\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    M=0\n",
                    "    @" + seg + "\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @" + str(ind) + "\n",
                    "    D=A\n",
                    "    @" + seg + "\n",
                    "    M=M-D\n"
                ]

            elif seg == "constant":
                return

            elif seg == "static":
                lst = [
                    "// pop static " + str(ind) + "\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    M=0\n",
                    "    @" + self.get_name() + ind + "\n",
                    "    M=D\n"
                ]

            elif seg == "temp":      # RAM 5 to 12
                lst = [
                    "// pop temp " + str(ind) + "\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    M=0\n",
                    "    @" + str(int(ind) + 5) + "\n",
                    "    M=D\n"
                ]

            elif seg == "pointer" and int(ind) in [0, 1]:
                if int(ind) == 0:  # THIS
                    lst = [
                        "// pop pointer 0\n",
                        "    @SP\n",
                        "    M=M-1\n",
                        "    A=M\n",
                        "    D=M\n",
                        "    @THIS\n",
                        "    M=D\n"
                    ]
                else:  # THAT
                    lst = [
                        "// pop pointer 1\n",
                        "    @SP\n",
                        "    M=M-1\n",
                        "    A=M\n",
                        "    D=M\n",
                        "    @THAT\n",
                        "    M=D\n"
                    ]

        self.output.writelines(lst)

    def close(self):
        """ Closes the .asm file """
        self.output.close()
