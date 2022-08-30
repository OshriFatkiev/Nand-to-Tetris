import CompilationEngine
import JackTokenizer
import os
import sys


def main(files):
    """ The main function of the Jack Compiler.
     responsible for tokenizing and compiline each .jack file """
    if isinstance(files, str):
        jack_tokenizer = JackTokenizer.JackTokenizer(files)
        jack_tokenizer.advance()
        filename = files.replace('jack', 'vm')
        compile_engine = CompilationEngine.CompilationEngine(jack_tokenizer, filename)
        if jack_tokenizer.tokens_list[0] == 'class':
            compile_engine.compile_class()

    elif isinstance(files, list):
        for file in files:
            jack_tokenizer = JackTokenizer.JackTokenizer(file)
            jack_tokenizer.advance()
            filename = file.replace('jack', 'vm')
            compile_engine = CompilationEngine.CompilationEngine(jack_tokenizer, filename)
            if jack_tokenizer.tokens_list[0] == 'class':
                compile_engine.compile_class()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()

    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)

    if not os.path.isfile(directory):
        directory = os.path.abspath(directory)

    if directory.endswith(".jack"):  # in case the dir is to specific .jack file
        main(directory)

    else:                            # in case the dir is to some folder
        files = []
        for filename in os.listdir(directory):
            if filename.endswith(".jack"):
                files.append(os.path.join(directory, filename))
        main(files)

