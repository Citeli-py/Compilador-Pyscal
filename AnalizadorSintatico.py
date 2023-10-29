Tokenlist=list()
Index=0
Token=None

class AnalizadorSintatico:
    def __init__(self, listaTokens) -> None:
        start(listaTokens)
        programa()

#ver caso quando acavba os tokens
def start(list):
    global Tokenlist, Token
    Tokenlist=list
    Token=list[0]

def next():
    global Tokenlist, Token, Index
    print(Token)
    tokenAnterior=Token

    if confere_tamanho():
        Tokenlist=Tokenlist[1:]
    else:
        return None
    
    Token=Tokenlist[0]
    Index += 1

    return tokenAnterior

def confere_tipo(type):
    global Tokenlist, Token
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
        print(f'Erro inesperado na linha {Token[2]}')
    elif esperado == None:
        print(f'Erro ({type}): Na linha {Token[2]}')

    print(f'Erro ({type}): Era esperado "{esperado}" na linha {Token[2]}')


def programa():
    no_0 = declaracoes()
    no_1 = bloco()
    return ('PROGRAMA', (no_0, no_1))
    
def declaracoes():
    no_0 = def_const()
    no_1 = def_tipo()
    no_2 = def_var()
    no_3 = def_rot()
    return ('DECLARACOES', (no_0, no_1, no_2, no_3))
    
def def_const(): #
    if confere_tipo('CONST'):
        no_0 = next()
        no_1 = constante()
        if confere_tipo('PONTOVIRGULA'): # erro
            no_2=next()
            no_3 =list_const()
            return ('DEF_CONST', (no_0, no_1, no_2, no_3))
        else:
            erro("DEF_CONST",";")

    return None

def list_const(): #
    no_0 = constante()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_const()
            return ('LIST_CONST', (no_0, no_1, no_2))
            
        else:
            erro("LIST_CONST",";")

    return None
    
def constante(): #
    if confere_tipo('ID'):
        no_0 = next() #ID
        if confere_tipo('IGUALIGUAL'):
            no_1 = next() #IGUALIGUAL
            no_2 = const_valor() #Numero ou string
            return ('CONSTANTE', (no_0, no_1, no_2))
        else:
            erro("CONSTANTE", "==")
    else:
        erro("CONSTANTE","ID") 
    
    return None
    
def const_valor():#
    if confere_tipo('NUMERO') or confere_tipo('ID'): # EXP_MAT
        no_0 = exp_mat()
        return ('EXP_MAT', (no_0))
    
    elif confere_tipo('STRING'):
        no_0 = exp_mat()
        return ('CONST_VALOR', (no_0))
    
    else:
        erro("CONST_VALOR", "STRING | EXP_MAT")
        

def def_tipo(): #
    if confere_tipo('TYPE'):
        no_0 = next()
        no_1 = tipo()
        if confere_tipo('PONTOVIRGULA'):
            no_2 = next()
            no_3 = list_tipos()
            return ('DEF_TIPO', (no_0, no_1, no_2, no_3))
        else:
            erro("PONTOVIRGULA",";")
    else:
        erro("TYPE","type")

def list_tipos(): #
    no_0 = tipo()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_tipos()
            return ('LIST_TIPOS', (no_0, no_1, no_2))
        else: 
            erro('PONTOVIRGULA', ';')
    
    return None

def tipo(): #
    if confere_tipo('ID'):
        no_0 = next()
        if confere_tipo('IGUALIGUAL'):
            no_1 = next()
            no_2 = tipo_dado()
            return ('TIPO', (no_0, no_1, no_2))
        else:
            erro('IGUALIGUAL','==')
    else:
        erro('ID','ID')
    
    return None



def tipo_dado():#
    if confere_tipo('INTEGER'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    elif confere_tipo('REAL'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    elif confere_tipo('ARRAY'):
        return array()

    elif confere_tipo('RECORD'):
        no_0 = next()
        no_1 = campos()
        if confere_tipo('END'):
            no_2 = next()
            return ('TIPO_DADO', (no_0, no_1, no_2))
        else:
            erro("TIPO_DADO","end")

    elif confere_tipo('ID'):
        no_0 = next()
        return ('TIPO_DADO', (no_0))
    
    else:
        erro("TIPO_DADO", "integer | real | array | record | ID")

    return None

def array(): # função auxiliar
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
                    return ('TIPO_DADO', (no_0, no_1, no_2, no_3, no_4, no_5))
                else:
                    erro('TIPO_DADO',"of")
            else:
                erro("TIPO_DADO","]")
        else:
            erro("TIPO_DADO","numero")
    else:
        erro("TIPO_DADO","[")
    
    return None
    
def campos(): #
    if confere_tipo ('ID'):
        no_0 = next()
        if confere_tipo('DOISPONTOS'):
            no_1 = next()
            no_2 = tipo_dado()
            no_3 = lista_campos()
            return ('CAMPOS', (no_0, no_1, no_2, no_3))
        else:
            erro("DOISPONTOS",":") 
    else:
        erro("CAMPOS","ID")
    
    return None

def lista_campos(): #
    if confere_tipo ('PONTOVIRGULA'):
        no_0 = next()
        no_1 = campos()
        no_2 = lista_campos()
        return ('LISTA_CAMPOS', (no_0, no_1, no_2))
    
    return None

def def_var(): #
    if confere_tipo('VAR'):
        no_0 = next()
        no_1 = variavel()
        if confere_tipo ('PONTOVIRGULA'):
            no_2 = next()
            no_3 = list_var
            return ('DEF_VAR', (no_0, no_1, no_2, no_3))
        else:
            erro("DEF_VAR", ";")

    return None

def list_var(): #
    no_0 = variavel()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = list_var()
            return ('LIST_VAR', (no_0, no_1, no_2))
        else:
           erro("LIST_VAR", ";")

    return None

def variavel(): #
    if confere_tipo('ID'):
        no_0 = next()
        no_1 = lista_id()
        if confere_tipo ('DOISPONTOS'):
            no_2 = next()
            no_3 = tipo_dado()
            return ('VARIAVEL', (no_0, no_1, no_2, no_3))
        else:
            erro("VARIAVEL",":")
            
    else:
        erro("VARIAVEL","ID")
    
    return None

def lista_id(): #
    if confere_tipo ('VIRGULA'):
        no_0 = next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = lista_id()
            return ('LISTA_ID', (no_0, no_1, no_2))
        else:
            erro("LISTA_ID", "ID")

    return None

def def_rot(): #
    no_0 = nome_rotina()
    if no_0 != None:
        no_1 = def_var()
        no_2 = bloco()
        no_3 = def_rot()
        return ('DEF_ROT', (no_0, no_1, no_2, no_3))
    
    return None

def nome_rotina(): #
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
        else:
            erro("NOME_ROTINA","ID")
            
    elif confere_tipo('PROCEDURE'):
        no_0 =next()
        if confere_tipo('ID'):
            no_1 = next()
            no_2 = param_rot()
            return ('NOME_ROTINA', (no_0, no_1, no_2))
        else:
            erro("NOME_ROTINA","ID")
        
    else:
        erro("NOME_ROTINA","function | procedure")

    return None


def param_rot(): #
    if confere_tipo('PARENTESIS_ESQ'):
        no_0 = next()
        no_1 = campos()
        if confere_tipo('PARENTESIS_DIR'):
            no_2 = next()
            return ('PARAM_ROT', (no_0, no_1, no_2))
        else:
            erro("PARAM_ROT",")")
            
    return None


def bloco(): #
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
        else:
            erro("BLOCO",";")

    elif confere_tipo('DOISPONTOS'):
        no_0 = next()
        no_1 = comando()
        return ('BLOCO', (no_0, no_1))
    
    else:
        erro("BLOCO", ": | begin")

    return None


def lista_com(): #
    no_0 = comando()
    if no_0 != None:
        if confere_tipo('PONTOVIRGULA'):
            no_1 = next()
            no_2 = lista_com()
            return ('LISTA_COM', (no_0, no_1, no_2))
        else:
            erro("LISTA_COM", ";")

    return None

def comando(): #
    if confere_tipo('ID'):
        no_0 =next()
        no_1 = nome()
        if confere_tipo('ATRIBUICAO'):
            no_2 = next()
            no_3 = exp_mat()
            return ('COMANDO', (no_0, no_1, no_2, no_3))
        else:
            erro("COMANDO", ":=")

    elif confere_tipo('WHILE'):
        no_0 = next()
        no_1 = exp_logica()
        if confere_tipo('DO'):
            no_2 = next()
            no_3 = bloco()
            return ('COMANDO', (no_0, no_1, no_2, no_3))
        else:
            erro("COMANDO","DO")

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

    else:
        erro('COMANDO', 'id | while | if | return | write | read')

    return None


def f_else(): #
    if confere_tipo('ELSE'):
        no_0 = next()
        no_1 = bloco()
        return ('ELSE', (no_0, no_1))
    
    return None


def lista_param(): #
    no_0 = parametro()
    if no_0 != None:
        if confere_tipo('VIRGULA'):
            no_1 = next()
            no_2 = lista_param()
            return ('LISTA_PARAM', (no_0, no_1, no_2))
    
        else:
            return ('LISTA_PARAM', (no_0))
    
    return None


def exp_logica(): #
    no_0 = exp_mat()
    no_1 = next()
    if confere_tipo('OP_LOGICO'):
        no_2 = exp_logica()
        return ('EXP_LOGICA', (no_0, no_1, no_2))
    
    else:
        return ('EXP_LOGICA', (no_0))

def exp_mat():#
    no_0 = parametro()
    no_1 = next()
    if confere_tipo('OP_MAT'):
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

    return None

def nome():#
    if confere_tipo('PONTO'):
        no_0 = next()
        if confere_tipo("ID"):
            no_1 = next()
            no_2 = nome()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME", "ID")

    elif confere_tipo('COLCHETE_ESQ'):
        no_0 = next()
        no_1 = parametro()
        if confere_tipo('COLCHETE_DIR'):
            no_2 = next()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME","]")

    elif confere_tipo('PARENTESIS_ESQ'):
        no_0 = next()
        no_1 = lista_param()
        if confere_tipo('PARENTESIS_DIR'):
            no_2 = next()
            return ('NOME', (no_0, no_1, no_2))
        else:
            erro("NOME",")")
    
    return None

