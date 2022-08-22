class Parser:
    """ This class responsible for parsing the assembly code"""

    def __init__(self, inp):
        """ The constructor of Parser class """
        self.f = open(inp, 'r')
        self.lines = []
        for line in self.f.readlines():
            if line != '\n' and line[0:2] != '//' and not line.isspace():
                self.lines.append(line)

        self.count = len(self.lines)
        self.current = self.lines[len(self.lines) - self.count].strip().strip("\n").split("//")[0]
        self.f.close()

    def has_more_commands(self):
        """ Return True if there are more lines of assembly code left """
        if self.count:
            return True
        return False

    def advance(self):
        """ Moves to the next line of code """
        self.count -= 1
        if self.count:
            self.current = self.lines[len(self.lines) - self.count].strip().strip("\n").split("//")[0]

    def command_type(self):
        """ Returns the command type """
        if self.current[0] == "@":
            return "A_COMMAND"
        elif "=" in self.current or ";" in self.current:
            return "C_COMMAND"
        elif self.current[0] == "(":
            return "L_COMMAND"

    def symbol(self):
        """ Returns the symbol of the current A command """
        return self.current.strip("@").strip()

    def dest(self):
        """ returns the destination of the current C command """
        if "=" in self.current:
            dst = self.current.split("=")[0]
            dst = ''.join(dst.split())
            return dst
        return 'null'

    def comp(self):
        """ Returns the computation of the current C command """
        if "=" in self.current:
            cmp = self.current.split("=")[1].split(";")[0]
        else:
            cmp = self.current.split(";")[0]
        cmp = ''.join(cmp.split())
        return cmp

    def jump(self):
        """ Returns the jump type of the current C command """
        jmp = "null"
        if ";" in self.current:
            jmp = self.current.split(";")[1]
        jmp = ''.join(jmp.split())
        return jmp