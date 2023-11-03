from analisadorLexico import AnalizadorLexico
from AnalisadorSintatico import AnalisadorSintatico
from sys import argv

file = open(argv[1], 'r')

code = file.read()

Lexer = AnalizadorLexico()
Lexer.tokenizar(code)
Lexer.printErros()

print(AnalisadorSintatico(Lexer.tokens_gerados).arvoreSintatica)