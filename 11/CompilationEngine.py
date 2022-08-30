from SymbolTable import *
from VMWriter import *

NEW_LINE = "\n"
OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP = ['-', '~']
KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']


class CompilationEngine:
    """ Class that effects the actual compilation output """

    def __init__(self, input, output):
        """ The CompilationEngine constructor """
        self.tokenizer = input
        self.vm_file = VMWriter(output)
        self.symbol_table = SymbolTable()
        self.i = 0
        self.class_name = ''
        self.current_function = ''
        self.return_type = ''
        self.is_void = False
        self.is_function = False
        self.is_constructor = False
        self.is_method = False
        self.is_array = False

    def generate_label(self):
        """ Generates a unique label """
        label = 'L' + str(self.i)
        self.i += 1
        return label

    def compile_class(self):
        """ Compiles a complete class """
        self.handle_keyword(['class'])
        self.class_name = self.tokenizer.current
        self.handle_identifier(False)
        self.handle_symbol('{')

        while self.tokenizer.current in ['static', 'field']:
            self.compile_class_var_dec()

        while self.tokenizer.current in ['constructor', 'function', 'method']:
            self.symbol_table.start_subroutine()
            self.compile_subroutine_dec()

        self.handle_symbol('}')

    def compile_class_var_dec(self):
        """ Compiles a static declaration or a field declaration """
        kind = self.handle_keyword(['static', 'field'])  # type is 'static' or 'field'
        type = self.type_helper()
        name = self.tokenizer.current
        self.symbol_table.define(name, type, kind)
        self.handle_identifier(False)

        while self.tokenizer.symbol() != ';':
            self.handle_symbol(',')
            name = self.tokenizer.current
            self.symbol_table.define(name, type, kind)
            self.handle_identifier(False)

        self.handle_symbol(';')

    def compile_subroutine_dec(self):
        """ Compiles a complete method, function or constructor """
        self.handle_keyword(['constructor', 'function', 'method'])

        if self.tokenizer.token_type() == 'IDENTIFIER':
            self.return_type = self.handle_identifier(False)
        elif self.tokenizer.token_type() == 'KEYWORD':
            self.is_void = False
            self.return_type = self.tokenizer.current
            self.handle_keyword()
        else:
            raise ValueError

        self.current_function = self.class_name + '.' + self.tokenizer.current
        self.handle_identifier(False)

        if self.is_method:
            self.symbol_table.define('this', self.class_name, 'arg')

        self.handle_symbol('(')
        self.compile_parameter_list()
        self.handle_symbol(')')

        self.compile_subroutine_body()

    def compile_parameter_list(self):
        """ Compiles parameter list """
        parameters_count = 0
        if self.tokenizer.current != ')':
            parameters_count += 1
            type = self.type_helper()
            name = self.tokenizer.current
            self.symbol_table.define(name, type, 'arg')
            self.handle_identifier(False)
            while self.tokenizer.current == ',':
                self.handle_symbol(',')
                parameters_count += 1
                type = self.type_helper()
                name = self.tokenizer.current
                self.symbol_table.define(name, type, 'arg')
                self.handle_identifier(False)
        return parameters_count

    def compile_subroutine_body(self):
        """ Compiles a subroutine's body """
        self.handle_symbol('{')

        while self.tokenizer.current == 'var':
            self.compile_var_dec()

        if self.is_constructor:
            n_locals = self.symbol_table.var_count('local')
            n_fields = self.symbol_table.var_count('field')
            self.vm_file.write_function(self.class_name + '.new', n_locals)
            self.vm_file.write_push('constant', n_fields)
            self.vm_file.write_call('Memory.alloc', 1)
            self.vm_file.write_pop('pointer', 0)
        else:
            n_locals = self.symbol_table.var_count('local')
            self.vm_file.write_function(self.current_function, n_locals)

        if self.is_method:
            self.vm_file.write_push('argument', 0)
            self.vm_file.write_pop('pointer', 0)

        while self.tokenizer.current != '}':
            self.compile_statements()

        self.handle_symbol('}')
        return self.symbol_table.var_count('local')

    def compile_var_dec(self):
        """ Compiles a var declaration """
        kind = self.handle_keyword()
        type = self.type_helper()
        name = self.tokenizer.current
        self.symbol_table.define(name, type, kind)
        self.handle_identifier(False)

        while self.tokenizer.symbol() == ',':
            self.handle_symbol(',')
            name = self.tokenizer.current
            self.symbol_table.define(name, type, kind)
            self.handle_identifier(False)

        self.handle_symbol(';')

    def compile_statements(self):
        """ Compiles a sequence of statements """
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

    def compile_let(self):
        """ Compiles a let statement """
        self.handle_keyword(['let'])
        kind, index = self.handle_identifier(True)

        if self.tokenizer.current == '[':
            self.is_array = True
            self.handle_symbol('[')
            self.compile_expression()
            self.handle_symbol(']')
            self.vm_file.write_push(kind, index)
            self.vm_file.write_arithmetic('ADD')

        self.handle_symbol('=')
        self.compile_expression()
        self.handle_symbol(';')

        if self.is_array:
            self.vm_file.write_pop('temp', 0)
            self.vm_file.write_pop('pointer', 1)
            self.vm_file.write_push('temp', 0)
            self.vm_file.write_pop('that', 0)

        if kind == 'field' and (bool(self.symbol_table.subroutine_table) or self.is_constructor):
            kind = 'this'
        if not self.is_array:
            self.vm_file.write_pop(kind, index)
        self.is_array = False

    def compile_if(self):
        """ Compiles an if statement """
        self.handle_keyword(['if'])

        label_one = self.generate_label()
        label_two = self.generate_label()

        self.handle_symbol('(')
        self.compile_expression()
        self.handle_symbol(')')

        self.vm_file.write_arithmetic('NOT')
        self.vm_file.write_if(label_one)

        self.handle_symbol('{')
        self.compile_statements()
        self.handle_symbol('}')

        self.vm_file.write_goto(label_two)

        if self.tokenizer.current == "else":
            self.handle_keyword(['else'])
            self.vm_file.write_label(label_one)
            self.handle_symbol('{')
            self.compile_statements()
            self.handle_symbol('}')

        else:
            self.vm_file.write_label(label_one)

        self.vm_file.write_label(label_two)

    def compile_while(self):
        """ Compiles a while statement """
        self.handle_keyword(['while'])

        label_one = self.generate_label()
        label_two = self.generate_label()

        self.vm_file.write_label(label_one)

        self.handle_symbol('(')
        self.compile_expression()
        self.vm_file.write_arithmetic('NOT')
        self.handle_symbol(')')

        self.vm_file.write_if(label_two)

        self.handle_symbol('{')
        self.compile_statements()
        self.handle_symbol('}')

        self.vm_file.write_goto(label_one)
        self.vm_file.write_label(label_two)

    def compile_do(self):
        """ Compiles a do statement """
        self.handle_keyword(['do'])
        self.subroutine_call_helper()
        self.handle_symbol(';')
        self.vm_file.write_pop('temp', 0)

    def compile_return(self):
        """ Compiles a return statement """
        self.handle_keyword(['return'])
        if self.tokenizer.current != ';':
            self.compile_expression()
        self.handle_symbol(';')
        if self.is_void:
            self.vm_file.write_push('constant', 0)
        self.vm_file.write_return()

        if self.is_constructor:
            self.is_constructor = False
        if self.is_function:
            self.is_function = False
        if self.is_method:
            self.is_method = False
        if self.is_void:
            self.is_void = False

    def compile_expression(self):
        """ Compiles an expression """
        self.compile_term()
        while self.tokenizer.current in OP:
            sym = self.handle_symbol(self.tokenizer.symbol())
            self.compile_term()
            self.write_arithmetic_exp(sym)

    def compile_term(self):
        """ Compiles a term """
        if self.tokenizer.next_token() in ['.', '('] and self.tokenizer.current not in ['~', '(', '-']:
            self.subroutine_call_helper()
        elif self.tokenizer.token_type() == 'INT_CONST':
            val = str(self.tokenizer.int_val())
            self.tokenizer.advance()
            self.code_write(val)
        elif self.tokenizer.token_type() == 'STRING_CONST':
            val = self.tokenizer.string_val()[4:]  # cutting of the 'STR.' prefix
            self.compile_string_const(val)
            self.tokenizer.advance()
            self.code_write(val)
        elif self.tokenizer.token_type() == 'KEYWORD':
            val = self.tokenizer.current
            if val == 'this':  # and self.is_constructor:
                self.vm_file.write_push('pointer', 0)
                self.handle_keyword()
            else:
                self.handle_keyword()
                self.code_write(val)
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            kind, index = self.handle_identifier(True)
            if self.tokenizer.current == '[':
                self.handle_symbol('[')
                self.compile_expression()
                self.handle_symbol(']')
                self.vm_file.write_push(kind, index)
                self.vm_file.write_arithmetic('ADD')
                self.vm_file.write_pop('pointer', 1)
                self.vm_file.write_push('that', 0)
            else:
                self.vm_file.write_push(kind, index)
        elif self.tokenizer.token_type() == 'SYMBOL':
            if self.tokenizer.current == '(':
                self.handle_symbol('(')
                self.compile_expression()
                self.handle_symbol(')')
            elif self.tokenizer.current in UNARY_OP:
                val = self.tokenizer.current
                self.handle_symbol(val)
                self.compile_term()
                self.code_write(val)

    def compile_expression_list(self):
        """ Compiles comma-separated list of expressions """
        expression_count = 0
        if self.tokenizer.current != ')':
            expression_count += 1
            self.compile_expression()
            while self.tokenizer.current == ',':
                self.handle_symbol(',')
                expression_count += 1
                self.compile_expression()
        return expression_count

    def handle_identifier(self, is_used):
        """ Handles an identifier occurrence """
        if self.tokenizer.token_type() != 'IDENTIFIER':
            raise ValueError
        else:
            index = -1
            name = self.tokenizer.identifier()
            kind = self.symbol_table.kind_of(name)
            type = self.symbol_table.type_of(name)
            if kind in ['local', 'argument', 'static', 'field']:
                index = str(self.symbol_table.index_of(name))
            elif kind is None:
                if bool(self.symbol_table.class_table):
                    kind = 'subroutine'
                else:
                    kind = 'class'
            self.tokenizer.advance()
            if is_used and index != -1:   # in case the var is being used
                return kind, index

    def handle_keyword(self, keyword=[]):
        """ Handles a keyword occurrence """
        if self.tokenizer.current not in keyword and keyword != []:
            raise ValueError
        else:
            val = self.tokenizer.current
            if val == 'void':
                self.is_void = True
            elif val == 'function':
                self.is_function = True
            elif val == 'constructor':
                self.is_constructor = True
            elif val == 'method':
                self.is_method = True
            self.tokenizer.advance()
            return val

    def handle_symbol(self, symbol=''):
        """ Handles a symbol occurrence """
        if symbol != self.tokenizer.current:
            raise ValueError
        else:
            sym = self.tokenizer.current
            self.tokenizer.advance()
            return sym

    def type_helper(self):
        """ Compiles a type to .vm """
        if self.tokenizer.current in ['int', 'char', 'boolean']:
            type = self.tokenizer.keyword()
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            type = self.tokenizer.identifier()
        else:
            raise ValueError
        self.tokenizer.advance()
        return type

    def subroutine_call_helper(self):
        """ Compiles subroutine call """
        subroutine_name = self.tokenizer.current
        self.handle_identifier(True)
        n_args = 0

        if self.tokenizer.current == '(':
            self.vm_file.write_push('pointer', 0)  # example: do draw();
            n_args += 1
            self.handle_symbol('(')
            n_args += self.compile_expression_list()
            self.handle_symbol(')')
            self.vm_file.write_call(self.class_name + '.' + subroutine_name, n_args)

        elif self.tokenizer.current == '.':
            self.handle_symbol('.')
            if subroutine_name in self.symbol_table.subroutine_table.keys():
                n_args += 1
                index = self.symbol_table.index_of(subroutine_name)
                segment = self.symbol_table.kind_of(subroutine_name)
                type = self.symbol_table.type_of(subroutine_name)
                self.vm_file.write_push(segment, index)
                subroutine_name = type + '.' + self.tokenizer.current
            elif subroutine_name in self.symbol_table.class_table.keys():
                n_args += 1
                index = self.symbol_table.index_of(subroutine_name)
                segment = self.symbol_table.kind_of(subroutine_name)
                if segment == 'field':
                    segment = 'this'
                    self.vm_file.write_push(segment, index)
                type = self.symbol_table.type_of(subroutine_name)
                subroutine_name = type + '.' + self.tokenizer.current
            else:
                subroutine_name += '.' + self.tokenizer.current
            self.handle_identifier(True)
            self.handle_symbol('(')
            n_args += self.compile_expression_list()
            self.handle_symbol(')')
            self.vm_file.write_call(subroutine_name, n_args)

    def compile_string_const(self, val):
        """ compiles a string const to vm language """
        self.vm_file.write_push('constant', len(val))
        self.vm_file.write_call('String.new', 1)
        for let in val:
            self.vm_file.write_push('constant', ord(let))
            self.vm_file.write_call('String.appendChar', 2)

    def code_write(self, exp):
        """ Responsible for the .vm code writing """
        if exp.isnumeric():
            self.vm_file.write_push('constant', exp)
        elif exp in self.symbol_table.class_table or exp in self.symbol_table.subroutine_table:
            self.write_var_exp(exp)
        elif any(i in exp for i in '+-*/&|<>='):
            self.write_arithmetic_exp(exp)
        elif any(i in exp for i in '~!'):
            self.write_unary_exp(exp)
        elif exp in ['true', 'false', 'null']:
            self.write_keyword_exp(exp)

        elif exp.find('(') != -1:  # function call
            exp = exp.strip()
            left_paren = exp.find('(')
            function_name = exp[left_paren-1]
            right_paren = exp.find(')')
            exp_list = exp[left_paren:right_paren-1].split(',')
            for exp in exp_list:
                self.code_write(exp)
            self.vm_file.write_call(function_name, len(exp_list))

    def find_symbol(self, exp):
        """ Finds the desired symbol name """
        operator, op_name = '', ''
        for elem in OP:  # ['+', '-', '*', '/', '&', '|', '<', '>', '=']
            if elem in exp:
                operator = elem
                if elem == '+':
                    op_name = 'ADD'
                    break
                elif elem == '-':
                    op_name = 'SUB'
                    break
                elif elem == '*':
                    op_name = '*'
                    break
                elif elem == '/':
                    op_name = '/'
                    break
                elif elem == '&':
                    op_name = 'AND'
                    break
                elif elem == '|':
                    op_name = 'OR'
                    break
                elif elem == '<':
                    op_name = 'LT'
                    break
                elif elem == '>':
                    op_name = 'GT'
                    break
                elif elem == '=':
                    op_name = 'EQ'
                    break
        return operator, op_name

    def write_var_exp(self, exp):
        """ Writes an expression with variable """
        segment = self.symbol_table.kind_of(exp)
        index = self.symbol_table.index_of(exp)
        if self.is_method and segment == 'field':
            self.vm_file.write_push('this', index)
        else:
            self.vm_file.write_push(segment, index)

    def write_arithmetic_exp(self, exp):
        """ Writes an arithmetic symbol """
        operator, op_name = self.find_symbol(exp)
        if op_name.isalpha():
            self.vm_file.write_arithmetic(op_name)
        else:
            if op_name == '*':
                self.vm_file.write_call('Math.multiply', 2)
            elif op_name == '/':
                self.vm_file.write_call('Math.divide', 2)

    def write_unary_exp(self, exp):
        """ Writes an unary symbol """
        if '~' in exp:
            self.code_write(exp.replace('~', ''))
            self.vm_file.write_arithmetic('NOT')
        else:
            self.code_write(exp.replace('-', ''))
            self.vm_file.write_arithmetic('NEG')

    def write_keyword_exp(self, exp):
        """ Writes a keyword expression """
        if exp == 'true':
            self.vm_file.write_push('constant', 0)
            self.vm_file.write_arithmetic('NOT')
        elif exp == 'false':
            self.vm_file.write_push('constant', 0)
        else:
            self.vm_file.write_push('constant', 0)




