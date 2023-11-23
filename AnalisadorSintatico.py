Tokenlist=list()
Index=0
Token=None

DEBUG = False

VERMELHO = "\033[1;31;40m"
BRANCO = "\033[0m"
VERDE = "\033[92m"

class AnalisadorSintatico:
    def __init__(self, listaTokens) -> None:
        start(listaTokens)
        self.arvoreSintatica = programa()

#ver caso quando acavba os tokens
def start(list):
    global Tokenlist, Token
    Tokenlist=list
    Token=list[0]

def next():
    global Tokenlist, Token, Index
    tokenAnterior=Token
    Tokenlist=Tokenlist[1:]
    if not(confere_tamanho()):
        Tokenlist = []
        Token = None
        return None
    
    Token=Tokenlist[0]
    Index += 1

    if DEBUG:
        print(VERDE+"Token atual:", Token, BRANCO)

    return tokenAnterior

def confere_tipo(type):
    global Tokenlist, Token
    if DEBUG:
        print(f"Confere: {Token} com {type}")

    if confere_tamanho() and (Token[0] == type): #token = (tipo, valor, linha)
        return True
    return False

def confere_tamanho():
     global Tokenlist
     if (len(Tokenlist) > 0):
          return True
     return False

def erro(type=None,esperado=None):
    global Token
    if (type==None) and (esperado==None):
        print(f'{VERMELHO}Erro inesperado na linha {Token[2]}{BRANCO}')
    elif esperado == None:
        print(f'{VERMELHO}Erro ({type}): Na linha {Token[2]}{BRANCO}')

    print(f'{VERMELHO}Erro ({type}): Era esperado "{esperado}" mas foi recebido "{Token[1]}" na linha {Token[2]}{BRANCO}')

def programa()->tuple:#conferido
    no_0 = declaracoes()
    no_1 = bloco()
    return ('PROGRAMA', (no_0, no_1))
    
def declaracoes()->tuple:#conferido
    no_0 = def_const()
    no_1 = def_tipo()
    no_2 = def_var()
    no_3 = def_rot()
    return ('DECLARACOES', (no_0, no_1, no_2, no_3))
    
def def_const()->tuple: #conferido
    if confere_tipo('CONST'):
        no_0 = next()
        no_1 = constante()
        if confere_tipo('PONTOVIRGULA'): # erro
            no_2=next()
            no_3 =list_const()
            return ('DEF_CONST', (no_0, no_1, no_2, no_3))
        else:
            erro("DEF_CONST",";")
            no_3 = list_const()
            return ('DEF_CONST', (no_0, no_1, None, no_3))

    return None

def list_const()->tuple: #conferido
    no_0 = constante()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_const()
            return ('LIST_CONST', (no_0, no_1, no_2))
            
        else:
            erro("LIST_CONST",";")
            no_2 = list_const()
            return ('LIST_CONST', (no_0, None, no_2))

    return None
    
def constante()->tuple: #conferido
    if confere_tipo('ID'): # Erro
        no_0 = next() #ID
        if confere_tipo('IGUALIGUAL'):
            no_1 = next() #IGUALIGUAL
            no_2 = const_valor() #Numero ou string
            return ('CONSTANTE', (no_0, no_1, no_2))
        else:
            erro("CONSTANTE", "==")
            no_2 = const_valor()
            return ('CONSTANTE', (no_0, None, no_2))
    #else:
    #    erro("CONSTANTE","ID") 
    
    return None
    
def const_valor()->tuple:#??
    if confere_tipo('NUMERO') or confere_tipo('ID'): # EXP_MAT
        no_0 = exp_mat()
        return ('CONST_VALOR', (no_0))
    
    elif confere_tipo('STRING'):
        no_0 = next()
        return ('CONST_VALOR', (no_0))
    
    else:
        erro("CONST_VALOR", "STRING | EXP_MAT")
        return ('CONST_VALOR', (None))
    
    return None   

def def_tipo(): # ver, def tipos pode retornar epslon,ver se e dessa forma(como em def const)
    if confere_tipo('TYPE'):
        no_0 = next()
        no_1 = tipo()
        if confere_tipo('PONTOVIRGULA'):
            no_2 = next()
            no_3 = list_tipos()
            return ('DEF_TIPO', (no_0, no_1, no_2, no_3))
        else:
            erro("PONTOVIRGULA",";")
            no_3 = list_tipos()
            return ('DEF_TIPO', (no_0, no_1, None, no_3))
    #else:
        #erro("TYPE","type")

    return None

def list_tipos(): #conferido
    no_0 = tipo()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_tipos()
            return ('LIST_TIPOS', (no_0, no_1, no_2))
        else: 
            erro('PONTOVIRGULA', ';')
            no_2 = list_tipos()
            return ('LIST_TIPOS', (no_0, None, no_2))
    
    return None

def tipo(): #conferido
    if confere_tipo('ID'):
        no_0 = next()
        if confere_tipo('IGUALIGUAL'):
            no_1 = next()
            no_2 = tipo_dado()
            return ('TIPO', (no_0, no_1, no_2))
        else:
            erro('IGUALIGUAL','==')
            no_2 = tipo_dado()
            return ('TIPO', (no_0, None, no_2))
    #else:
    #    erro('ID','ID')
    
    return None

def tipo_dado():#conferido
    if confere_tipo('INTEGER'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    elif confere_tipo('REAL'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    elif confere_tipo('ARRAY'):
        no_0 =array()
        return ('TIPO_DADO', (no_0))

    elif confere_tipo('RECORD'):
        no_0 = next()
        no_1 = campos()
        if confere_tipo('END'):
            no_2 = next()
            return ('TIPO_DADO', ('RECORD', (no_0, no_1, no_2)))
        else:
            erro("TIPO_DADO","end")
            return ('TIPO_DADO', ('RECORD', (no_0, no_1, None)))

    elif confere_tipo('ID'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    else:
        erro("TIPO_DADO", "integer | real | array | record | ID")
        # Tipo dado termina com ';', 'VAR' ou 'ID'
        while not(confere_tipo('VAR') or confere_tipo('PONTOVIRGULA') or confere_tipo("ID")):
            next()


    return None

def array(): # função auxiliar começa com next? se outra função chamar sem ser tipo dado da erro
    no_0 = next()
    if confere_tipo('COLCHETE_ESQ'):
        no_1 = next()
        if confere_tipo('NUMERO'):
            no_2 = next()
            if confere_tipo('COLCHETE_DIR'):
                no_3 = next()
                if confere_tipo('OF'):
                    no_4 = next()
                    no_5 = tipo_dado()
                    return ('ARRAY', (no_0, no_1, no_2, no_3, no_4, no_5))
                else:
                    erro('ARRAY',"of")
                    no_5 = tipo_dado()
                    return ('ARRAY', (no_0, no_1, no_2, no_3, None, no_5))
            else:
                erro("ARRAY","]")
                return ('ARRAY', (no_0, no_1, no_2, None, None, None))
        else:
            erro("ARRAY","numero")
            return ('ARRAY', (no_0, no_1, None, None, None, None))
    else:
        erro("ARRAY","[")
        return ('ARRAY', (no_0, None, None, None, None, None))
    
    return None
    
def campos(): #
    if confere_tipo('ID'):
        no_0 = next()
        if confere_tipo('DOISPONTOS'):
            no_1 = next()
            no_2 = tipo_dado()
            no_3 = lista_campos()
            return ('CAMPOS', (no_0, no_1, no_2, no_3))
        else:
            erro("DOISPONTOS",":") 
            no_2 = tipo_dado()
            no_3 = lista_campos()
            return ('CAMPOS', (no_0, None, no_2, no_3))
    else:
        erro("CAMPOS","ID")
        no_2 = tipo_dado()
        no_3 = lista_campos()
        return ('CAMPOS', (None, no_1, no_2, no_3))
    
    return None

def lista_campos(): # campos dentro de lista campos gera recursão?
    if confere_tipo ('PONTOVIRGULA'):
        no_0 = next()
        no_1 = campos()
        no_2 = lista_campos()
        return ('LISTA_CAMPOS', (no_0, no_1, no_2))
    
    return None

def def_var(): #conferido
    if confere_tipo('VAR'):
        no_0 = next()
        no_1 = variavel()
        if confere_tipo ('PONTOVIRGULA'):
            no_2 = next()
            no_3 = list_var()
            return ('DEF_VAR', (no_0, no_1, no_2, no_3))
        else:
            erro("DEF_VAR", ";")
            no_3 = list_var()
            return ('DEF_VAR', (no_0, no_1, None, no_3))

    return None

def list_var(): #conferido
    no_0 = variavel()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_var()
            return ('LIST_VAR', (no_0, no_1, no_2))
        else:
            erro("LIST_VAR", ";")
            no_2 = list_var()
            return ('LIST_VAR', (no_0, None, no_2))

    return None

def variavel(): #conferido
    if confere_tipo('ID'):
        no_0 = next()
        no_1 = lista_id()
        if confere_tipo ('DOISPONTOS'):
            no_2 = next()
            no_3 = tipo_dado()
            return ('VARIAVEL', (no_0, no_1, no_2, no_3))
        else:
            erro("VARIAVEL",":")
            no_3 = tipo_dado()
            return ('VARIAVEL', (no_0, no_1, None, no_3))
            
    
    return None

def lista_id(): #conferido
    if confere_tipo ('VIRGULA'):
        no_0 = next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = lista_id()
            return ('LISTA_ID', (no_0, no_1, no_2))
        else:
            erro("LISTA_ID", "ID")
            no_2 = lista_id()
            return ('LISTA_ID', (no_0, None, no_2))

    return None

def def_rot(): #conferido
    no_0 = nome_rotina()
    if no_0 != None:
        no_1 = def_var()
        no_2 = bloco()
        no_3 = def_rot()
        return ('DEF_ROT', (no_0, no_1, no_2, no_3))
    
    return None

def nome_rotina(): #conferido
    if confere_tipo ('FUNCTION'):
        no_0 = next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = param_rot()
            if confere_tipo('DOISPONTOS'):
                no_3 =next()
                no_4 = tipo_dado()
                return ('NOME_ROTINA', (no_0, no_1, no_2, no_3, no_4))
            else:
                erro("NOME_ROTINA",":")
                no_4 = tipo_dado()
                return ('NOME_ROTINA', (no_0, no_1, no_2, None, no_4))
        else:
            erro("NOME_ROTINA","ID")
            return ('NOME_ROTINA', (no_0, no_1, no_2, None, None))
            
            
    elif confere_tipo('PROCEDURE'):
        no_0 =next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = param_rot()
            return ('NOME_ROTINA', (no_0, no_1, no_2))
        else:
            erro("NOME_ROTINA","ID")
            no_2 = param_rot()
            return ('NOME_ROTINA', (no_0, None, no_2))
        

    return None

def param_rot(): #conferido
    if confere_tipo('PARENTESIS_ESQ'):
        no_0 = next()
        no_1 = campos()
        if confere_tipo('PARENTESIS_DIR'):
            no_2 = next()
            return ('PARAM_ROT', (no_0, no_1, no_2))
        else:
            erro("PARAM_ROT",")")
            return ('PARAM_ROT', (no_0, no_1, None))
            
    return None

def bloco(): #conferido
    if confere_tipo('BEGIN'):
        no_0 = next()
        no_1 = comando()
        if confere_tipo('PONTOVIRGULA'):
            no_2 = next()
            no_3 = lista_com()
            if confere_tipo('END'):
                no_4 = next()
                return ('BLOCO', (no_0, no_1, no_2, no_3, no_4))
            else:
                erro("BLOCO","END")
                return ('BLOCO', (no_0, no_1, no_2, no_3, None))
        else:
            erro("BLOCO",";")
            no_3 = lista_com()
            return ('BLOCO', (no_0, no_1, None, no_3, None))


    elif confere_tipo('DOISPONTOS'):
        no_0 = next()
        no_1 = comando()
        return ('BLOCO', (no_0, no_1))
    
    # else:
    #     erro("BLOCO", ": | begin")

    return None

def lista_com(): #conferido 
    no_0 = comando()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = lista_com()
            return ('LISTA_COM', (no_0, no_1, no_2))
        else:
            erro("LISTA_COM", ";")
            no_2 = lista_com()
            return ('LISTA_COM', (no_0, None, no_2))

    return None

def comando(): #não pussi exp_mat, ideal é fazer função atrib
    if confere_tipo('ID'):
        no_0 = next()   # ID
        no_1 = nome()   # nome
        no_2 = atrib()  # atrib
        return ('COMANDO', (no_0, no_1, no_2))

    elif confere_tipo('WHILE'):
        no_0 = next()
        no_1 = exp_logica()
        if confere_tipo('DO'):
            no_2 = next()
            no_3 = bloco()
            return ('COMANDO', (no_0, no_1, no_2, no_3))
        else:
            erro("COMANDO","DO")
            no_3 = bloco()
            return ('COMANDO', (no_0, no_1, None, no_3))

    elif confere_tipo('IF'):
        no_0 = next()
        no_1 = exp_logica()
        if confere_tipo('THEN'):
            no_2 =next()
            no_3 = bloco()
            no_4 = f_else()
            return ('COMANDO', (no_0, no_1, no_2, no_3, no_4))
        else:
            erro("COMANDO","then")
            no_3 = bloco()
            no_4 = f_else()
            return ('COMANDO', (no_0, no_1, None, no_3, no_4))

    elif confere_tipo('RETURN'):
        no_0 = next()
        no_1 = exp_logica()
        return ('COMANDO', (no_0, no_1))
    
    elif confere_tipo ('WRITE'):
        no_0 = next()
        no_1 = exp_mat()
        return ('COMANDO', (no_0, no_1))
    
    elif confere_tipo('READ'):
        no_0 = next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = nome()
            return ('COMANDO', (no_0, no_1, no_2))
        else:
            erro("COMANDO","ID")
            no_2 = nome()
            return ('COMANDO', (no_0, None, no_2))
    
    elif confere_tipo("RETURN"):
        no_0 = next()
        no_1 = exp_logica()
        return ("COMANDO", (no_0, no_1))
    
    elif Token == None: #Caso acabam os tokens
        return None

    # else:
    #     erro('COMANDO', 'id | while | if | return | write | read')

    return None

def atrib():
    if confere_tipo('ATRIBUICAO'):
        no_0=next()
        no_1=exp_mat()
        return("ATRIB",(no_0,no_1))
    return None

def f_else(): #
    if confere_tipo('ELSE'):
        no_0 = next()
        no_1 = bloco()
        return ('ELSE', (no_0, no_1))
    
    return None

def lista_param(): #conferida

    # Situação de função sem parametro
    if confere_tipo("PARENTESIS_DIR"):
        return None

    no_0 = parametro()
    if no_0 != None:
        if confere_tipo('VIRGULA'):
            no_1 = next()
            no_2 = lista_param()
            return ('LISTA_PARAM', (no_0, no_1, no_2))
    
        else:
            return ('LISTA_PARAM', (no_0))
    
    return None

def exp_logica(): #next dps do exp_mat
    no_0 = exp_mat()
    if confere_tipo('OP_LOGICO'): #ver se precisa de função para o OP logico
        no_1 = next()
        no_2 = exp_logica()
        return ('EXP_LOGICA', (no_0, no_1, no_2))
    
    else:
        return ('EXP_LOGICA', (no_0))

def exp_mat():#
    no_0 = parametro()
    if confere_tipo('OP_MAT'):
        no_1 = next()
        no_2 = exp_mat()
        return ('EXP_MAT', (no_0, no_1, no_2))
    
    else:
        return ('EXP_MAT', (no_0))

def parametro():#
    if confere_tipo('ID'):
        no_0 = next()
        no_1 = nome()
        return ('PARAMETRO', (no_0, no_1))
    
    elif confere_tipo('NUMERO'):
        no_0 = next()
        return ('PARAMETRO', (no_0))
    
    else:
        erro("PARAMETRO", "ID | NUMERO")
        return ('PARAMETRO', (None))

    return None

def nome():##conferida
    if confere_tipo('PONTO'):
        no_0 = next()
        if confere_tipo("ID"):
            no_1 = next()
            no_2 = nome()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME", "ID")
            no_2 = nome()
            return ('NOME', (no_0, None, no_2))

    elif confere_tipo('COLCHETE_ESQ'):
        no_0 = next()
        no_1 = parametro()
        if confere_tipo('COLCHETE_DIR'):
            no_2 = next()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME","]")
            return ('NOME', (no_0, no_1, None))

    elif confere_tipo('PARENTESIS_ESQ'):
        no_0 = next()
        no_1 = lista_param()
        if confere_tipo('PARENTESIS_DIR'):
            no_2 = next()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME",")")
            return ('NOME', (no_0, no_1, None))
    
    return None

