
class SymbolTable:
    """ This class creates table object for the symbols """

    def __init__(self):
        """ The class constructor """
        self.d = dict()

    def add_entry(self, symbol, int):
        """ Adds a new symbol to the table  with his unique number """
        self.d.update({symbol: int})

    def contains(self, symbol):
        """ Returns True if the table contains the symbol, False otherwise """
        if symbol in self.d.keys():
            return True
        return False

    def get_address(self, symbol):
        """ Returns the symbol unique number, if exists """
        for key, value in self.d.items():
            if symbol == key:
                return value
        return -1
