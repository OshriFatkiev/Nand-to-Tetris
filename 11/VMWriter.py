class VMWriter:
    """ This class manages the .VM output file"""

    def __init__(self, output_file):
        """ The VMWriter constructor """
        self.output_file = open(output_file, 'w')

    def write_push(self, segment, index):
        """ writes push command """
        if segment == 'CONST':
            segment = 'CONSTANT'
        elif segment == 'var':
            segment = 'local'
        elif segment == 'field':
            segment = 'this'
        self.output_file.write('push ' + segment.lower() + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        """ writes pop command """
        if segment == 'CONST':
            segment = 'CONSTANT'
        elif segment == 'var':
            segment = 'local'
        elif segment == 'field':
            segment = 'this'
        self.output_file.write('pop ' + segment.lower() + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        """ writes an arithmetic command """
        self.output_file.write(command.lower() + '\n')

    def write_label(self, label):
        """ writes label command """
        self.output_file.write('label ' + label + '\n')

    def write_goto(self, label):
        """ writes goto command """
        self.output_file.write('goto ' + label + '\n')

    def write_if(self, label):
        """ writes if command """
        self.output_file.write('if-goto ' + label + '\n')

    def write_call(self, name, n_args):
        """ writes call command """
        self.output_file.write('call ' + name + ' ' + str(n_args) + '\n')

    def write_function(self, name, n_locals):
        """ writes function declaration """
        self.output_file.write('function ' + name + ' ' + str(n_locals) + '\n')

    def write_return(self):
        """ writes return command """
        self.output_file.write('return' + '\n')

    def close(self):
        """ closes the output .vm file """
        self.output_file.close()
