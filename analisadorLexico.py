import ply.lex as lex

class AnalizadorLexico:
    # TOKEN{ type, value, lineno, lexpos }
    palavras_reservadas = {
        'if': 'IF',
        'else': 'ELSE',
        'begin': 'BEGIN',
        'end': 'END',
        'const': 'CONST',
        'integer': 'INTEGER',
        'record': 'RECORD',
        'of': 'OF',
        'real': 'REAL',
        'array': 'ARRAY',
        'var': 'VAR',
        'type': 'TYPE',
        'function': 'FUNCTION',
        'procedure': 'PROCEDURE',
        'write': 'WRITE',
        'read': 'READ',
        'then': 'THEN',
        'do': 'DO',

        'id': 'ID' # Caso não seja uma palavra reservada
    }

    tokens = [
        'OP_LOGICO',
        'OP_MAT',
        'NUMERO',
        'STRING',
        'CONST_VALOR',
        'COMENTARIO',
        'PONTOVIRGULA',
        'DOISPONTOS',
        'ATRIBUICAO',
        'PONTO',
        'COLCHETE_ESQ',
        'COLCHETE_DIR',
        'PARENTESIS_ESQ',
        'PARENTESIS_DIR',
        'VIRGULA',
        'IGUALIGUAL',
    ] + list(palavras_reservadas.values())


    t_NUMERO = r'[0-9]+(\.[0-9]*)?'
    t_STRING = r'\".*\"'
    t_OP_MAT = r'[\+|\-|\*|\/]'
    t_OP_LOGICO = r'[<|>|!|=]' 

    t_PONTOVIRGULA = r'\;'
    t_DOISPONTOS = r'\:'
    t_ATRIBUICAO = r':='
    t_PONTO = r'\.'
    t_VIRGULA = r'\,'
    t_COLCHETE_ESQ = r'\['
    t_COLCHETE_DIR = r'\]'
    t_PARENTESIS_ESQ = r'\('
    t_PARENTESIS_DIR = r'\)'

    def t_IGUALIGUAL(self, token: lex.LexToken) -> lex.LexToken:
        r'=='
        return token

    def t_ID(self, token: lex.LexToken) -> lex.LexToken: #Um identificador pode se confundir com uma palavra reservada
        r'[a-zA-Z][a-zA-Z0-9_]*'
        token.type = self.palavras_reservadas.get(token.value,'ID')    # Checa palavras reservadas
        return token

    def t_newline(self,token: lex.LexToken)-> None:
        r'\n+'
        token.lexer.lineno += len(token.value)

    def t_COMENTARIO(self, token: lex.LexToken) -> None:
        r'//.*'
        pass

    def t_COMENTARIO_MULTILINHA(self, token: lex.LexToken) -> None:
        r"\/\*(\*(?!\/)|[^*])*\*\/"
        token.lexer.lineno += token.value.count("\n") # Coreção do numero de linhas
        pass

    t_ignore  = ' \t'

    def t_error(self, token: lex.LexToken) -> None:
        self.erros_gerados.append((token.value, token.lineno))
        token.lexer.skip(1)

    def __init__(self,) -> None:
        '''
            token = (tipo, valor, linha)
        '''
        self.lexer = lex.lex(module=self)
        self.tokens_gerados = list()
        self.erros_gerados = list()

    def addToken(self, token: lex.LexToken) -> None:
        self.tokens_gerados.append((token.type, token.value, token.lineno))

    
    def tokenizar(self, programa: str) -> None:
        self.lexer.input(programa)

        while True:
            token = self.lexer.token()
            if not token:
                break

            self.addToken(token)

    def printTokens(self,):
        for token in self.tokens_gerados:
            print(f"{token[0]} {(15-len(token[0]))*' '} linha: {token[2]} {(3-len(str(token[2])))*' '} {token[1]}")
    
    def printErros(self, ):
        for token in self.erros_gerados:
            print("\033[1;31;40m"+ 
                f"Caracter ilegal '{token[0][0]}' na linha {token[1]}" 
                + "\033[0m")

