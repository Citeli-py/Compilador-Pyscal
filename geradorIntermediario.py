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


class Gerador:

    def __init__(self, programa, arvore_sintatica) -> None:
        self.arvore = arvore_sintatica
        self.temp = 0
        self.label = 0
        self.arquivo = open(f"{programa}class", "w")

        declaracoes = self.arvore[1][0]
        bloco = self.arvore[1][1]

        self.percorrerArvore(declaracoes)
        self.write("LBL main")
        self.percorrerArvore(bloco)
    
    def percorrerArvore(self, no):
        if isinstance(no, tuple):
            for filho in no:
                if isinstance(filho, tuple):
                    if self.regras(filho):
                        #print(filho, end="\n\n")
                        self.percorrerArvore(filho)
    
    def write(self, comando):
        self.arquivo.write(f"{comando}\n")

    def labelAtual(self, ):
        return self.label-1
    
    def getLabel(self, ):
        self.label += 1
        return self.label-1

    def tempAtual(self,):
        #if self.temp > 0:
        return f"temp{self.temp-1}"
        #return "temp0"
    
    def getTemp(self, ):
        self.temp += 1
        return f"temp{self.temp-1}"
    
    def regras(self, no):
        if no[0] == 'CONSTANTE':
            id_esq = no[1][0][1]
            if no[1][2][1][0] == "STRING":
                id_dir = no[1][2][1][1]
            else:
                id_dir = no[1][2][1][1][1][1]
            
            self.write(f"ATR {id_esq}, {id_dir}")
            return False
        
        elif no[0] == "COMANDO":
            #print(no)
            if no[1][0][0] == "READ":
                identificador = no[1][1][1]
                self.write(f"RED {identificador}")
            
            elif no[1][0][0] == "WRITE":
                identificador = no[1][1][1][1][0][1]
                self.write(f"WRT {identificador}")
            
            elif no[1][0][0] == "ID": 
                if no[1][2] == None and no[1][1] != None: # Chamada de função ou procedure
                    if no[1][1][1][1] != None: # Com prametros
                        identificador = no[1][0][1]
                        self.chamadaFunc(no, identificador)
                
                elif no[1][2] != None:
                    id_esq = no[1][0][1]
                    exp_mat = no[1][2][1][1]
                    self.exp_math(exp_mat)
                    self.write(f"ATR {id_esq}, {self.tempAtual()}")
            
            elif no[1][0][0] == "RETURN":
                # Depois tratar com expressão logica
                self.write(f"RTN {no[1][1][1][1][1][0][1]}")
            
            elif no[1][0][0] == "IF":
                label = self.getLabel()
                self.write(f"LBL if{label}")

                if no[1][4] != None: # Tem else
                    self.exp_logica(no[1][1], f"f_else{label}")
                    bloco = no[1][3]
                    self.bloco(bloco)
                    self.write(f"LBL else{label}")
                    self.Else(no[1][4])

                else:
                    self.exp_logica(no[1][1], f"f_if{label}")
                    bloco = no[1][3]
                    self.bloco(bloco)

                self.write(f"LBL f_if{label}")
            
            elif no[1][0][0] == "WHILE":
                label = self.getLabel()
                self.write(f"LBL while{label}")
                self.exp_logica(no[1][1], f"f_while{label}")
                self.bloco(no[1][3])
                self.write(f"JMP while{label}")
                self.write(f"LBL f_while{label}")

            return False
        
        elif no[0] == "NOME_ROTINA":
            self.write(f"LBL {no[1][1][1]}")

            if no[1][0][0] == "FUNCTION":
                self.declaraFunc(no[1][2])
            
            return False
        

        return True
    
    def Else(self, no):
        bloco = no[1][1]
        self.bloco(bloco)
    
    def bloco(self, no):
        self.percorrerArvore(no)
        '''print(no)
        if no[1][3] != None:
            self.percorrerArvore(no[1][3])'''
    
    def conta_param(self, no, valor):
        contador = 0
        if no[0] == valor:
            return 1
        
        else:
            for filho in no:
                if isinstance(filho, tuple):
                    contador += self.conta_param(filho, valor)

        return contador
    
    def declaraFunc(self, no):
        '''
        GPR a
        GPR b
        '''
        campos = no[1][1][1]
        self.write(f"GPR {campos[0][1]}")
        
        while campos[3] != None:
            campos = campos[3][1][1][1]
            self.write(f"GPR {campos[0][1]}")

    def chamadaFunc(self, no, nome): # Melhor juntar com a função de cima tornando criar parametros recursiva
        '''
        PRM a
        PRM b
        JMP func
        GRN t1
        '''
        lista_params = no[1][1][1][1]
        num_parametros = self.conta_param(lista_params, "PARAMETRO")
        for i in range(num_parametros-1):
            param = lista_params[1][0][1]
            self.write(f"PRM {param[0][1]}")
            lista_params = lista_params[1][2]

        param = lista_params[1][1]
        self.write(f"PRM {param[0][1]}")
        self.write(f"JMP {nome}")

        temp = self.getTemp()
        self.write(f"GRN {temp}")
        return temp
    
    def exp_math(self, no):
        tam_exp = self.conta_param(no, "PARAMETRO")
        
        operandos = []
        prox = no

        for i in range(tam_exp):
            if prox[1][0] == "PARAMETRO":
                if isinstance(prox[1][1][1], tuple): # Funcão
                    temp = self.chamadaFunc(prox[1], prox[1][1][0][1])
                    operandos.append(temp) # tem que dar append em um temporario

                elif prox[1][1][0] == "NUMERO": # NUMERO
                    operandos.append(prox[1][1][1])
                    #printg(prox[1][1][1])

                elif prox[1][1][0][0] == "ID":
                    operandos.append(prox[1][1][0][1])

            else: # PARAMETRO
                if prox[1][0][1][0] != "NUMERO":
                    operandos.append(prox[1][0][1][0][1])
                else:
                    operandos.append(prox[1][0][1][1])

            
            if i < (tam_exp-1):
                operandos.append(prox[1][1][1])
                prox = prox[1][2]
        
        return self.exp_mat_comandos(operandos)

    def exp_mat_comandos(self, operandos):

        if len(operandos) == 1:
            self.write(f"ATR {self.getTemp()}, {operandos[0]}")
        
        else:
            while len(operandos) > 2:
                if operandos[1] == "+":
                    self.write(f"ADD {self.getTemp()}, {operandos[0]}, {operandos[2]}")
                elif operandos[1] == "-":
                    self.write(f"SUB {self.getTemp()}, {operandos[0]}, {operandos[2]}")
                elif operandos[1] == "*":
                    self.write(f"MLT {self.getTemp()}, {operandos[0]}, {operandos[2]}")
                elif operandos[1] == "/":
                    self.write(f"DIV {self.getTemp()}, {operandos[0]}, {operandos[2]}")
                
                else:
                    printv("Tem algo muito errado em exp_mat_comandos")
                
                operandos = self.shiftList(operandos)
        
        return self.tempAtual()

    def shiftList(self, lista):
        novaLista = [self.tempAtual()]
        for i in range(len(lista)-3):
            novaLista.append(lista[i+3])
        
        return novaLista
        
    def exp_logica(self, no, jumpLabel):
        exp_esq = no[1][0]
        operador = no[1][1][1]
        exp_dir = no[1][2][1]
        temp_esq = self.exp_math(exp_esq)
        temp_dir = self.exp_math(exp_dir)

        if operador == "=":
            self.write(f"JNE {jumpLabel}, {temp_esq}, {temp_dir}")
        elif operador == ">":
            self.write(f"JGT {jumpLabel}, {temp_dir}, {temp_esq}")
        elif operador == "!":
            self.write(f"JEQ {jumpLabel}, {temp_esq}, {temp_dir}")
        elif operador == "<":
            self.write(f"JGT {jumpLabel}, {temp_esq}, {temp_dir}")
        else:
            print("Algo deu errado em exp_logica!")
