
class Parser:
    """ Handles the parsing of a single .vm file """

    def __init__(self, inp):
        """ The constructor of Parser class """
        self.f = open(inp, 'r')
        self.lines = []
        for line in self.f.readlines():
            if line != '\n' and line[0:2] != '//' and not line.isspace():
                if "\t" in line:
                    line = line.replace("\t", "")
                line = line.split('//')[0]
                line = line.split()
                self.lines.append(line)

        self.count = len(self.lines)
        self.line_num = len(self.lines) - self.count
        self.current = self.lines[self.line_num]
        self.f.close()

    def has_more_commands(self):
        """ Return true if there are more .vm lines left, false otherwise """
        if self.count:
            return True
        return False

    def advance(self):
        """ Moves one line forward """
        self.count -= 1
        self.line_num = len(self.lines) - self.count
        if self.count:
            self.current = self.lines[self.line_num]

    def command_type(self):
        """ Return the command type """
        arithmetic_lst = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if self.current[0] in arithmetic_lst:
            return "C_ARITHMETIC"
        elif self.current[0] == "push":
            return "C_PUSH"
        elif self.current[0] == "pop":
            return "C_POP"
        elif self.current[0] == "label":
            return "C_LABEL"
        elif self.current[0] == "if-goto":
            return "C_IF"
        elif self.current[0] == "goto":
            return "C_GOTO"
        elif self.current[0] == "function":
            return "C_FUNCTION"
        elif self.current[0] == "call":
            return "C_CALL"
        elif self.current[0] == "return":
            return "C_RETURN"

    def arg1(self):
        """ Returns the first argument """
        if self.command_type() == "C_RETURN":
            return
        if self.command_type() == "C_ARITHMETIC":
            return self.current[0]
        return self.current[1]

    def arg2(self):
        """ Returns the second argument """
        arg_lst = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]
        if self.command_type() in arg_lst:
            return self.current[2]


