NEW_LINE = "\n"
OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP = ['-', '~']
KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']


def _keyword(string):
    """ Returns the xml format of the given keyword """
    return "<keyword> " + string + " </keyword>" + NEW_LINE


def _symbol(symbol):
    """ Returns the xml format of the given symbol """
    return "<symbol> " + symbol + " </symbol>" + NEW_LINE


def _identifier(string):
    """ Returns the xml format of the given identifier """
    return "<identifier> " + string + " </identifier>" + NEW_LINE


def _int_const(string):
    """ Returns the xml format of the given integer constant """
    return "<integerConstant> " + string + " </integerConstant>" + NEW_LINE


def _str_const(string):
    """ Returns the xml format of the given string constant """
    return "<stringConstant> " + string + " </stringConstant>" + NEW_LINE


class CompilationEngine:
    """ Class that effects the actual compilation output """

    def __init__(self, input, output):
        """ The CompilationEngine constructor """
        self.tokenizer = input
        self.output_file = open(output, 'w')
        self.i = 0
        self.indent = " " * 4 * self.i

    def compile_class(self):
        """ Compiles a complete class """
        self.init_state('class')
        self.handle_keyword(['class'])
        self.handle_identifier()
        self.handle_symbol('{')

        while self.tokenizer.current in ['static', 'field']:
            self.compile_class_var_dec()

        while self.tokenizer.current in ['constructor', 'function', 'method']:
            self.compile_subroutine_dec()

        self.handle_symbol('}')
        self.close_state('class')
        self.output_file.close()

    def compile_class_var_dec(self):
        """ Compiles a static declaration or a field declaration """
        self.init_state('classVarDec')
        self.handle_keyword(['static', 'field'])
        self.type_helper()
        self.handle_identifier()

        while self.tokenizer.symbol() != ';':
            self.handle_symbol(',')
            self.handle_identifier()

        self.handle_symbol(';')
        self.close_state('classVarDec')

    def compile_subroutine_dec(self):
        """ Compiles a complete method, function or constructor """
        self.init_state('subroutineDec')
        self.handle_keyword(['constructor', 'function', 'method'])

        if self.tokenizer.token_type() == 'IDENTIFIER':
            self.handle_identifier()
        elif self.tokenizer.token_type() == 'KEYWORD':
            self.handle_keyword()
        else:
            raise ValueError

        self.handle_identifier()
        self.handle_symbol('(')

        self.compile_parameter_list()
        self.handle_symbol(')')

        self.compile_subroutine_body()
        self.close_state('subroutineDec')

    def compile_parameter_list(self):
        """ Compiles parameter list """
        self.init_state('parameterList')

        if self.tokenizer.current != ')':
            self.type_helper()
            self.handle_identifier()
            while self.tokenizer.current == ',':
                self.handle_symbol(',')
                self.type_helper()
                self.handle_identifier()

        self.close_state('parameterList')

    def compile_subroutine_body(self):
        """ Compiles a subroutine's body """
        self.init_state('subroutineBody')
        self.handle_symbol('{')

        while self.tokenizer.current == 'var':
            self.compile_var_dec()

        while self.tokenizer.current != '}':
            self.compile_statements()

        self.handle_symbol('}')
        self.close_state('subroutineBody')

    def compile_var_dec(self):
        """ Compiles a var declaration """
        self.init_state('varDec')

        self.handle_keyword()
        self.type_helper()
        self.handle_identifier()

        while self.tokenizer.symbol() == ',':
            self.handle_symbol(',')
            self.handle_identifier()

        self.handle_symbol(';')
        self.close_state('varDec')

    def compile_statements(self):
        """ Compiles a sequence of statements """
        self.init_state('statements')

        while self.tokenizer.current in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.current == 'let':
                self.compile_let()
            elif self.tokenizer.current == 'if':
                self.compile_if()
            elif self.tokenizer.current == 'while':
                self.compile_while()
            elif self.tokenizer.current == 'do':
                self.compile_do()
            elif self.tokenizer.current == 'return':
                self.compile_return()

        self.close_state("statements")

    def compile_let(self):
        """ Compiles a let statement """
        self.init_state("letStatement")
        self.handle_keyword(['let'])
        self.handle_identifier()

        if self.tokenizer.current == '[':
            self.handle_symbol('[')
            self.compile_expression()
            self.handle_symbol(']')

        self.handle_symbol('=')
        self.compile_expression()
        self.handle_symbol(';')
        self.close_state("letStatement")

    def compile_if(self):
        """ Compiles an if statement """
        self.init_state('ifStatement')
        self.handle_keyword(['if'])

        self.handle_symbol('(')
        self.compile_expression()
        self.handle_symbol(')')

        self.handle_symbol('{')
        self.compile_statements()
        self.handle_symbol('}')

        if self.tokenizer.current == "else":
            self.handle_keyword(['else'])
            self.handle_symbol('{')
            self.compile_statements()
            self.handle_symbol('}')

        self.close_state('ifStatement')

    def compile_while(self):
        """ Compiles a while statement """
        self.init_state("whileStatement")
        self.handle_keyword(['while'])

        self.handle_symbol('(')
        self.compile_expression()
        self.handle_symbol(')')

        self.handle_symbol('{')
        self.compile_statements()
        self.handle_symbol('}')

        self.close_state("whileStatement")

    def compile_do(self):
        """ Compiles a do statement """
        self.init_state("doStatement")
        self.handle_keyword(['do'])
        self.subroutine_call_helper()
        self.handle_symbol(';')
        self.close_state("doStatement")

    def compile_return(self):
        """ Compiles a return statement """
        self.init_state("returnStatement")
        self.handle_keyword(['return'])
        if self.tokenizer.current != ';':
            self.compile_expression()
        self.handle_symbol(';')
        self.close_state("returnStatement")

    def compile_expression(self):
        """ Compiles an expression """
        self.init_state('expression')
        self.compile_term()
        while self.tokenizer.current in OP:
            self.handle_symbol(self.tokenizer.symbol())
            self.compile_term()
        self.close_state('expression')

    def compile_term(self):
        """ Compiles a term """
        self.init_state('term')
        if self.tokenizer.next_token() in ['.', '('] and self.tokenizer.current not in ['~', '(', '-']:
            self.subroutine_call_helper()
        elif self.tokenizer.token_type() == 'INT_CONST':
            text = self.indent + _int_const(str(self.tokenizer.int_val()))
            self.output_file.write(text)
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'STRING_CONST':
            text = self.indent + _str_const(self.tokenizer.string_val()[4:])  # cutting of the 'STR.' prefix
            self.output_file.write(text)
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'KEYWORD':
            self.handle_keyword()
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            self.handle_identifier()
            if self.tokenizer.current == '[':
                self.handle_symbol('[')
                self.compile_expression()
                self.handle_symbol(']')
        elif self.tokenizer.token_type() == 'SYMBOL':
            if self.tokenizer.current == '(':
                self.handle_symbol('(')
                self.compile_expression()
                self.handle_symbol(')')
            elif self.tokenizer.current in UNARY_OP:
                self.handle_symbol(self.tokenizer.current)
                self.compile_term()

        self.close_state('term')

    def compile_expression_list(self):
        """ Compiles comma-separated list of expressions """
        self.init_state('expressionList')

        if self.tokenizer.current != ')':
            self.compile_expression()
            while self.tokenizer.current == ',':
                self.handle_symbol(',')
                self.compile_expression()

        self.close_state('expressionList')

    def init_state(self, headline):
        """ Writes <headline> at the beginning of the current XML section """
        self.output_file.write("<" + headline + ">" + NEW_LINE)
        self.i += 1

    def close_state(self, headline):
        """ Writes </headline> at the end of the current XML section """
        self.i -= 1
        self.output_file.write("</" + headline + ">" + NEW_LINE)

    def handle_identifier(self):
        """ Handles an identifier occurrence """
        if self.tokenizer.token_type() != 'IDENTIFIER':
            raise ValueError
        else:
            text = self.indent + _identifier(self.tokenizer.identifier())
            self.output_file.write(text)
            self.tokenizer.advance()

    def handle_keyword(self, keyword=[]):
        """ Handles a keyword occurrence """
        if self.tokenizer.current not in keyword and keyword != []:
            raise ValueError
        else:
            text = self.indent + _keyword(self.tokenizer.keyword())
            self.output_file.write(text)
            self.tokenizer.advance()

    def handle_symbol(self, symbol=''):
        """ Handles a symbol occurrence """
        if symbol != self.tokenizer.current:
            raise ValueError
        else:
            if self.tokenizer.current == '<':
                text = self.indent + _symbol('&lt;')
            elif self.tokenizer.current == '>':
                text = self.indent + _symbol('&gt;')
            elif self.tokenizer.current == '"':
                text = self.indent + _symbol('&quot;')
            elif self.tokenizer.current == '&':
                text = self.indent + _symbol('&amp;')
            else:
                text = self.indent + _symbol(self.tokenizer.symbol())
            self.output_file.write(text)
            self.tokenizer.advance()

    def type_helper(self):
        """ Compiles a type to .xml """
        if self.tokenizer.current in ['int', 'char', 'boolean']:
            text = self.indent + _keyword(self.tokenizer.keyword())
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            text = self.indent + _identifier(self.tokenizer.identifier())
        else:
            raise ValueError
        self.output_file.write(text)
        self.tokenizer.advance()

    def subroutine_call_helper(self):
        """ Compiles subroutine call """
        self.handle_identifier()

        if self.tokenizer.current == '(':
            self.handle_symbol('(')
            self.compile_expression_list()
            self.handle_symbol(')')

        elif self.tokenizer.current == '.':
            self.handle_symbol('.')
            self.handle_identifier()
            self.handle_symbol('(')
            self.compile_expression_list()
            self.handle_symbol(')')

