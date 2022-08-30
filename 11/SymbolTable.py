class SymbolTable:
    """ THis class responsible for crating ang manipulating the symbol table """

    def __init__(self):
        """ The SymbolTable constructor """
        self.class_table = {}
        self.subroutine_table = {}
        self.class_index = {'static': 0, 'field': 0}
        self.subroutine_index = {'argument': 0, 'local': 0}

    def start_subroutine(self):
        """ clears the subroutine table """
        self.subroutine_table.clear()
        self.subroutine_index = {'argument': 0, 'local': 0}

    def define(self, name, type, kind):
        """ adds a new value to the relevant symbol table """
        if kind in ['static', 'field']:
            self.class_table[name] = (type, kind, self.class_index[kind])
            self.class_index[kind] += 1
        elif kind in ['arg', 'var']:
            if kind == 'var':
                kind = 'local'
            if kind == 'arg':
                kind = 'argument'
            self.subroutine_table[name] = (type, kind, self.subroutine_index[kind])
            self.subroutine_index[kind] += 1

    def var_count(self, kind):
        """ return the num of kind 'kind' in the relevant symbol table """
        i = 0
        for key, value in self.class_table.items():
            if value[1] == kind:
                i += 1
        for key, value in self.subroutine_table.items():
            if value[1] == kind:
                i += 1
        return i

    def kind_of(self, name):
        """ return the kind of 'name' """
        for key, value in self.subroutine_table.items():
            if key == name:
                return value[1]
        for key, value in self.class_table.items():
            if key == name:
                return value[1]
        return None

    def type_of(self, name):
        """ return the type of 'name' """
        if not bool(self.class_table):   # in case the class table empty
            if not bool(self.subroutine_table):
                return 'class'
            else:
                for key, value in self.subroutine_table.items():
                    if key == name:
                        return value[0]
                return 'subroutine'
        else:
            for key, value in self.class_table.items():
                if key == name:
                    return value[0]

    def index_of(self, name):
        """ return the index of 'name' """
        for key, value in self.subroutine_table.items():
            if key == name:
                return value[2]
        for key, value in self.class_table.items():
            if key == name:
                return value[2]


