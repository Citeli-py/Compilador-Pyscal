from analisadorLexico import AnalizadorLexico
from AnalizadorSintatico import AnalizadorSintatico
from sys import argv

file = open(argv[1], 'r')

code = file.read()

Lexer = AnalizadorLexico()
Lexer.tokenizar(code)
Lexer.printErros()

linha = 0
for token in Lexer.tokens_gerados:
    if linha < token[2]:
        linha = token[2]
        print()

    print(token, end='')

print("\n\n++++ Sintatico +++++\n")
AnalizadorSintatico(Lexer.tokens_gerados)