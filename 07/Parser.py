
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
                    line = line.replace(" ", "")
                self.lines.append(line)

        self.count = len(self.lines)
        self.current = self.lines[len(self.lines) - self.count].strip().strip("\n").split("//")[0]
        self.f.close()

    def has_more_commands(self):
        """ Return true if there are more .vm lines left, false otherwise """
        if self.count:
            return True
        return False

    def advance(self):
        """ Moves one line forward """
        self.count -= 1
        if self.count:
            self.current = self.lines[len(self.lines) - self.count].strip().strip("\n").split("//")[0]

    def command_type(self):
        """ Return the command type """
        arithmetic_lst = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if self.current in arithmetic_lst:
            return "C_ARITHMETIC"
        elif "push" in self.current:
            return "C_PUSH"
        elif "pop" in self.current:
            return "C_POP"
        elif "label" in self.current:
            return "C_LABEL"
        elif "goto" in self.current:
            return "C_GOTO"
        elif "if" in self.current:
            return "C_IF"
        elif "function" in self.current:
            return "C_FUNCTION"
        elif "call" in self.current:
            return "C_RETURN"
        elif "return" in self.current:
            return "C_CALL"

    def arg1(self):
        """ Returns the first argument """
        if self.command_type() == "C_RETURN":
            return
        if self.command_type() == "C_ARITHMETIC":
            return self.current
        return self.current.split()[1]

    def arg2(self):
        """ Returns the second argument """
        arg_lst = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]
        if self.command_type() in arg_lst:
            return self.current.split()[2]


