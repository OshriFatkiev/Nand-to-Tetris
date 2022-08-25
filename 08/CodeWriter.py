import os

ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"
PUSH = "push"
POP = "pop"

LCL = "LCL"
ARG = "ARG"
THIS = "THIS"
THAT = "THAT"
BOOTSTRAP = "BOOTSTRAP"


class CodeWriter:
    """ Translates VM commands into Hack assembly code """

    def __init__(self, out):
        """ The CodeWriter constructor """
        if not os.path.exists(out):
            self.output = open(out, 'w')
            self.write_init()
        else:
            self.output = open(out, 'a')

    def write_init(self):
        """ The bootstrap code """
        lst = [
            "// " + BOOTSTRAP + "\n",
            "    @256\n",
            "    D=A\n",
            "    @SP\n",
            "    M=D\n"
        ]
        self.output.writelines(lst)
        self.write_call("Sys.init", 0, 0)

    def get_name(self):
        """ Returns the name of the file """
        return os.path.basename(self.output.name).strip("asm")

    def write_arithmetic(self, cmd, parser, current_function):
        """ Converts the arithmetic commands to Assembly """
        lst = []

        if cmd == ADD:
            lst = [
                "// " + ADD.upper() + "\n",
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
                "// " + SUB.upper() + "\n",
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
                "// " + NEG.upper() + "\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    M=-M\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd == AND:
            lst = [
                "// " + AND.upper() + "\n",
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
                "// " + OR.upper() + "\n",
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
                "// " + NOT.upper() + "\n",
                "    @SP\n",
                "    M=M-1\n",
                "    A=M\n",
                "    M=!M\n",
                "    @SP\n",
                "    M=M+1\n"
            ]

        elif cmd in [EQ, GT, LT]:

            x_sign = current_function + ".x_sign." + str(parser.line_num)      # making sure no label occurs twice
            same_sign = current_function + ".same_sign." + str(parser.line_num)
            true = current_function + ".true." + str(parser.line_num)
            false = current_function + ".false." + str(parser.line_num)
            end = current_function + ".end." + str(parser.line_num)

            jump, jump_two = '', ''
            if cmd == GT:
                jump = "JGT"
                jump_two = "JLE"
            elif cmd == LT:
                jump = "JLT"
                jump_two = "JGE"

            if cmd == GT or cmd == LT:

                lst = [
                    "// " + cmd.upper() + "\n",
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
                    "// " + cmd.upper() + "\n",
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

    def write_push_pop(self, cmd, seg, ind, current_vm_file):
        """ Write push and pop command in Assembly """
        lst = []

        if cmd == "C_PUSH":

            if seg in ["local", "argument", "this", "that"]:
                if seg == "local":
                    seg = LCL
                elif seg == "argument":
                    seg = ARG
                elif seg == "this":
                    seg = THIS
                else:
                    seg = THAT

                lst = [
                    "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
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
                    "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
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
                    "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
                    "    @" + current_vm_file + "." + str(ind) + "\n",
                    "    D=M\n",
                    "    @SP\n",
                    "    A=M\n",
                    "    M=D\n",
                    "    @SP\n",
                    "    M=M+1\n"
                ]

            elif seg == "temp":  # RAM 5 to 12
                lst = [
                    "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
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
                        "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
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
                        "// " + PUSH.upper() + " " + seg + " " + str(ind) + "\n",
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
                    seg = LCL
                elif seg == "argument":
                    seg = ARG
                elif seg == "this":
                    seg = THIS
                else:
                    seg = THAT

                lst = [
                    "// " + POP.upper() + " " + seg + " " + str(ind) + "\n",
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
                    "// " + POP.upper() + " " + seg + " " + str(ind) + "\n",
                    "    @SP\n",
                    "    M=M-1\n",
                    "    A=M\n",
                    "    D=M\n",
                    "    M=0\n",
                    "    @" + current_vm_file + "." + str(ind) + "\n",
                    "    M=D\n"
                ]

            elif seg == "temp":      # RAM 5 to 12
                lst = [
                    "// " + POP.upper() + " " + seg + " " + str(ind) + "\n",
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
                        "// " + POP.upper() + " " + seg + " " + str(ind) + "\n",
                        "    @SP\n",
                        "    M=M-1\n",
                        "    A=M\n",
                        "    D=M\n",
                        "    @THIS\n",
                        "    M=D\n"
                    ]
                else:  # THAT
                    lst = [
                        "// " + POP.upper() + " " + seg + " " + str(ind) + "\n",
                        "    @SP\n",
                        "    M=M-1\n",
                        "    A=M\n",
                        "    D=M\n",
                        "    @THAT\n",
                        "    M=D\n"
                    ]

        self.output.writelines(lst)

    def write_label(self, label):
        """ Writes the assembly translation of the label command """
        self.output.writelines([
            "// LABEL\n",
            "(" + label + ")\n"
        ])

    def write_goto(self, label):
        """ Writes the assembly translation of the goto command """
        lst = [
            "// GOTO " + label + "\n",
            "    @" + label + "\n",
            "    0;JMP\n",
        ]
        self.output.writelines(lst)

    def write_if(self, label):
        """ Writes the assembly translation of the if-goto command """
        lst = [
            "// IF_GOTO " + label + "\n",
            "    @SP\n",
            "    M=M-1\n",
            "    A=M\n",
            "    D=M\n",
            "    @" + label + "\n",
            "    D;JNE\n"
        ]
        self.output.writelines(lst)

    def write_call(self, function_name, args_num, count):
        """ Writes the assembly translation of the given call command """
        return_address = function_name+"$ret."+str(count)
        lst = [
            "// CALL " + function_name + " " + str(args_num) + "\n",
            "//  __push return address\n",
            "    @" + return_address + "\n",
            "    D=A\n",
            "    @SP\n",
            "    A=M\n",
            "    M=D\n",
            "    @SP\n",
            "    M=M+1\n"
        ]
        self.output.writelines(lst)
        self.push_helper(LCL)
        self.push_helper(ARG)
        self.push_helper(THIS)
        self.push_helper(THAT)
        lst = [
            "//  __ARG = SP - (n_args + 5)\n",
            "    @SP\n",
            "    D=M\n",
            "    @" + str(args_num) + "\n",
            "    D=D-A\n",
            "    @5\n",
            "    D=D-A\n",
            "    @ARG\n"
            "    M=D\n",
            "//  __LCL = SP\n",
            "    @SP\n",
            "    D=M\n",
            "    @LCL\n",
            "    M=D\n",
        ]
        self.output.writelines(lst)
        self.write_goto(function_name)
        self.write_label(return_address)

    def push_helper(self, arg):
        """ Pushes the content of arg to the 'main' stack in Assembly """
        lst = [
            "    @" + arg + "\n",
            "    D=M\n",
            "    @SP\n",
            "    A=M\n",
            "    M=D\n",
            "    @SP\n",
            "    M=M+1\n"
        ]
        self.output.writelines(lst)

    def write_function(self, function_name, locals_num):
        """ Writes the assembly translation of the function command """
        self.write_label(function_name)
        self.output.write("// FUNCTION: " + function_name + "\n")
        for i in range(int(locals_num)):
            lst = [
                "    @SP\n",
                "    A=M\n",
                "    M=0\n",
                "    @SP\n",
                "    M=M+1\n",
            ]
            self.output.writelines(lst)

    def write_return(self):
        """ Writes the assembly translation of the return command """
        lst = [
            "// RETURN\n",
            "//  __end_frame = LCL\n",
            "    @LCL\n",
            "    D=M\n",
            "    @end_frame\n",
            "    M=D\n"
            "//  __ret = *(end_frame-5)\n",
            "    @5\n",
            "    D=D-A\n",
            "    A=D\n",
            "    D=M\n",
            "    @return\n",
            "    M=D\n"
            "//  __*ARG = pop()\n",
            "    @SP\n",
            "    M=M-1\n",
            "    A=M\n",
            "    D=M\n",   # D = return value
            "    @ARG\n",
            "    A=M\n",
            "    M=D\n",
            "//  __SP = ARG + 1\n",
            "    @ARG\n",
            "    D=M+1\n",
            "    @SP\n",
            "    M=D\n",
            "//  __THAT = *(end_frame-1)\n",
            "    @end_frame\n",
            "    D=M-1\n",
            "    A=D\n",
            "    D=M\n",
            "    @THAT\n",
            "    M=D\n",
        ]
        self.output.writelines(lst)

        self.return_helper(THIS, 2)
        self.return_helper(ARG, 3)
        self.return_helper(LCL, 4)

        lst = [
            "//  __goto return\n",
            "    @return\n",
            "    A=M\n",
            "    0;JMP\n"
        ]
        self.output.writelines(lst)

    def return_helper(self, arg, num):
        """ Sub-function to write_return function """
        lst = [
            "//  __" + arg + " = *(end_frame- " + str(num) + ")\n",
            "    @" + str(num) + "\n",
            "    D=A\n",
            "    @end_frame\n",
            "    D=M-D\n",
            "    A=D\n",
            "    D=M\n",
            "    @" + arg + "\n",
            "    M=D\n"
        ]
        self.output.writelines(lst)

    def close(self):
        """ Closes the .asm file """
        self.output.close()
