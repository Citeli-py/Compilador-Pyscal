
# (Nome, Classificação, Tipo, Escopo, Quantidade, Ordem)

VERMELHO = "\033[1;31;40m"
BRANCO = "\033[0m"
VERDE = "\033[92m"

def printg(*txt):
    aux = ''
    for t in txt:
        aux+= str(t) + ' '
    print(VERDE+aux+BRANCO)

def printv(*txt):
    aux = ''
    for t in txt:
        aux+= str(t) + ' '
    print(VERMELHO+aux+BRANCO)

class TabelaSimbolos:
    def __init__(self) -> None:
        self.simbolos = {}
    
    def add(self, simbolo) -> None: #Melhorar isso ai, criar um simbolo em cada função
        # (Nome, Classificação, Tipo, Escopo, Quantidade, Ordem)
        if simbolo[0] not in self.simbolos.keys():
            self.simbolos[(simbolo[0], simbolo[3])] = simbolo
            printg(simbolo)
        else:
            print(f"Erro: Já existe o ID {simbolo[0]} em {simbolo[3]}")

    def lookup(self, nome, escopo):
       res = self.simbolos.get((nome, escopo)) 
       if res == None:
           res = self.simbolos.get((nome, 'GLOBAL'))
       return res


class AnalisadorSemantico:

    def __init__(self) -> None:
        self.Tabela = TabelaSimbolos()
        self.escopo = "GLOBAL"

    def semantico(self, no): # Separar entre declarações, rotinas e bloco main para lidar com escopo
        if isinstance(no, tuple):
            for filho in no:
                if isinstance(filho, tuple):
                    self.escopoAtual(filho)
                    self.regras(filho)
                    self.semantico(filho)
    
    def escopoAtual(self, no): # Função pra trocar de escopo
        if no[0] == "DEF_ROT":
            self.escopo = no[1][0][1][1][1]
    
    def regras(self, no):
        if no[0] == 'CONSTANTE':
            self.constante(no[1])
        
        elif no[0] == "TIPO":
            self.tipo(no[1])
        
        elif no[0] == 'VARIAVEL':
            self.variavel(no[1])

        elif no[0] == 'ID': # Verifica se o ID existe na tabela
            # Falta inteligencia aqui
            if self.Tabela.lookup(no[1], self.escopo) == None:
                # Problema com IDs em RECORDS
                printv(f"ERRO: {no} não foi declarado!")

        else:
            pass

    
    def constante(self, no):
        # nome, CONSTANTE, CONSTANTE, escopo, None, None 
        simbolo = (no[0][1], 'CONSTANTE', 'CONSTANTE', self.escopo, None, None) 
        self.Tabela.add(simbolo)
    
    def tipo(self, no):
        # nome, TIPO, tipo, escopo, qtd, NONE 
        tipo_tipo = self.tipo_dado(no[2])
        simbolo = (no[0][1], "TIPO", tipo_tipo[0], self.escopo, tipo_tipo[1], None)
        self.Tabela.add(simbolo)

    def variavel(self, no):
        # nome, VARIAVEL, tipo, escopo, qtd, ordem 
        printv(no)
        if no[1] == None: # Variavel sozinha
            var_tipo = self.tipo_dado(no[3])
            simbolo = (no[0][1], "VARIAVEL", var_tipo[0], self.escopo, var_tipo[1], None)
            self.Tabela.add(simbolo)
        
        else:
            # Percorrer a lista id e ir adicionando na tabela
            pass
        

    def record(self, no):
        campos = no[1][1][1][1]

        simbolos_campos = []
        tipo_record = self.tipo_dado(campos)
        simbolos_campos.append((campos[0][1], 'CAMPO', tipo_record[0], self.escopo, tipo_record[1], None))

        prox_campo = campos
        while prox_campo[3] != None:
            prox_campo = prox_campo[3][1][1][1]
            tipo_record = self.tipo_dado(prox_campo)
            simbolos_campos.append((prox_campo[0][1], 'CAMPO', tipo_record[0], self.escopo, tipo_record[1], None))

        return 'RECORD', simbolos_campos

    def array(self, no, ):
        return no[1][1][5][1][0], no[1][1][2][1] 


    def tipo_dado(self, no_tipo_dado): # Retorna o tipo e a qtd de um dado
        if no_tipo_dado[1][0] == 'ARRAY':
            # nome, clas, tipo, escopo, qtd, ordem 
            return self.array(no_tipo_dado)

        elif no_tipo_dado[1][0] == 'RECORD':
            # nome, TIPO, RECORD, escopo, [campos], None
            return self.record(no_tipo_dado)

        elif no_tipo_dado[1][0] == "ID": # Se no for um record
            return no_tipo_dado[1][1], None 

        else:
            return no_tipo_dado[1][0], None  
