class JackTokenizer:
    """ Tokenizing the .jack file """

    KEYWORD = [
        "class",
        "constructor",
        "function",
        "method",
        "field",
        "static",
        "var",
        "int",
        "char",
        "boolean",
        "void",
        "true",
        "false",
        "null",
        "this",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return"
    ]

    SYMBOL = [
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+",
        "-", "*", "/", "&", "|", "<", ">", "=", "~"
    ]

    def __init__(self, input_file):
        """ The constructor of the tokenizer instance """
        self.jack_file = open(input_file, 'r')
        self.tokens_list = []
        self.get_tokens(self.jack_file)
        self.current = ""
        self.index = -1

    def get_tokens(self, file):
        """ Gets all the tokens from the .jack file """
        lines = file.readlines()
        open_quotes = False
        open_comment = False
        for line in lines:

            if line == '' or line.isspace():  # empty line
                continue

            line = line.strip()
            line_string = ''
            string_const = 'STR.'
            for i, char in enumerate(line):

                if open_comment and char != '/':
                    continue
                elif open_quotes and char != '"':
                    string_const += char

                elif char == '/':
                    if not open_comment:
                        if i < len(line)-1:
                            if line[i+1] == '/':
                                break
                            elif line[i+1] == '*':
                                open_comment = True
                            else:
                                line_string += char
                    else:  # open_comment = True
                        if i > 1:
                            if line[i-1] == '*':
                                open_comment = False
                        elif i == len(line)-1:
                            open_comment = False

                elif char == '"':
                    self.tokenize_line(line_string)
                    line_string = ''
                    if not open_quotes:
                        open_quotes = True
                    else:
                        open_quotes = False
                        self.tokens_list.append(string_const)
                        string_const = 'STR.'
                else:
                    line_string += char

            self.tokenize_line(line_string)

    def has_more_tokens(self):
        """ Returns True if there are more tokens, False otherwise """
        if self.index < len(self.tokens_list)-1:
            return True
        return False

    def advance(self):
        """ Move on to the next token in the token_list """
        if self.index != len(self.tokens_list)-1:
            self.index += 1
            self.current = self.tokens_list[self.index]

    def token_type(self):
        """ Returns the current token type """
        if self.current in JackTokenizer.KEYWORD:
            return "KEYWORD"
        elif self.current in JackTokenizer.SYMBOL:
            return "SYMBOL"
        elif self.current.isidentifier() and 'STR.' not in self.current:
            return "IDENTIFIER"
        elif self.current.isnumeric():
            return "INT_CONST"
        else:       # string constant:
            return "STRING_CONST"

    def keyword(self):
        """ Returns the keyword, in case the current token is a keyword """
        for key in JackTokenizer.KEYWORD:
            if self.current == key:
                return key

    def symbol(self):
        """ Returns the symbol, in case the current token is a symbol """
        for sym in JackTokenizer.SYMBOL:
            if self.current == sym:
                return sym

    def identifier(self):
        """ Returns the identifier, in case the current token is an identifier """
        return self.current

    def int_val(self):
        """ Returns the integer constant, in case the current token is an integer constant """
        return int(self.current)

    def string_val(self):
        """ Returns the string constant, in case the current token is a string constant """
        return self.current.strip('"')

    def next_token(self):
        """ Returns the next token """
        if self.index < len(self.tokens_list)-1:
            return self.tokens_list[self.index+1]

    def tokenize_line(self, line):
        """ Tokenizes entire line into her specific terminals """

        line = line.split()

        for element in line:

            if element in JackTokenizer.KEYWORD:
                self.tokens_list.append(element)
            elif element.isnumeric():
                self.tokens_list.append(element)
            elif element.isalpha():
                self.tokens_list.append(element)
            else:
                string = ''
                for char in element:
                    if char in JackTokenizer.SYMBOL:
                        if element != char and string != '':
                            self.tokens_list.append(string)
                            string = ''
                        self.tokens_list.append(char)
                    elif char == '"':
                        pass
                    else:
                        string += char
                if string != '':
                    self.tokens_list.append(string)


