DEST_DICT = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

COMP_DICT = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
    "D<<": "0110000",
    "D>>": "0010000",
    "A<<": "0100000",
    "A>>": "0000000",
    "M<<": "1100000",
    "M>>": "1000000"
}

JUMP_DICT = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def dest(string):
    """ Returns the destination represents string in binary """
    for key, value in DEST_DICT.items():
        if key == string:
            return value


def comp(string):
    """ Returns the computation represents string in binary """
    for key, value in COMP_DICT.items():
        if key == string:
            return value


def jump(string):
    """ Returns the jump represents string in binary """
    for key, value in JUMP_DICT.items():
        if key == string:
            return value
