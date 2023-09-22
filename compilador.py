from analisadorLexico import AnalizadorLexico
from sys import argv

file = open(argv[1], 'r')

code = file.read()

Lexer = AnalizadorLexico()
Lexer.tokenizar(code)
Lexer.printTokens()