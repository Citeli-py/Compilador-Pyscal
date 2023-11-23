from analisadorLexico import AnalizadorLexico
from AnalisadorSintatico import AnalisadorSintatico
from analisadorSemantico import AnalisadorSemantico
from sys import argv

file = open(argv[1], 'r')

code = file.read()

Lexer = AnalizadorLexico()
Lexer.tokenizar(code)
Lexer.printErros()

Parser = AnalisadorSintatico(Lexer.tokens_gerados)
print(Parser.arvoreSintatica)

Semantico = AnalisadorSemantico()

Semantico.semantico(Parser.arvoreSintatica)
print(Semantico.Tabela.simbolos)