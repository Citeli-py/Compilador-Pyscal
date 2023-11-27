
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
        if (simbolo[0], simbolo[3]) not in self.simbolos.keys():
            self.simbolos[(simbolo[0], simbolo[3])] = simbolo
            #printg(simbolo)
            return True
    
        printv(f"Erro: Já existe o ID {simbolo[0]} em {simbolo[3]}")
        return False

    def lookup(self, nome, escopo):
       res = self.simbolos.get((nome, escopo)) 
       if res == None:
           res = self.simbolos.get((nome, 'GLOBAL'))
       return res


class AnalisadorSemantico:

    def __init__(self, arvore) -> None:
        self.Tabela = TabelaSimbolos()
        self.escopo = "GLOBAL"
        self.ArvoreSintatica = arvore

    def semantico(self,):
        declaracoes = self.ArvoreSintatica[1][0]
        bloco = self.ArvoreSintatica[1][1]

        self.semantico_r(declaracoes)
        self.escopo = "MAIN"
        self.semantico_r(bloco)

    def semantico_r(self, no): # Separar entre declarações, rotinas e bloco main para lidar com escopo
        if isinstance(no, tuple):
            for filho in no:
                if isinstance(filho, tuple):
                    self.escopoAtual(filho)
                    if self.regras(filho):
                        self.semantico_r(filho)
    
    def escopoAtual(self, no): # Função pra trocar de escopo
        if no[0] == "DEF_ROT":
            self.escopo = no[1][0][1][1][1]
    
    def regras(self, no):

        if no[0] == 'CONSTANTE':
            self.constante(no[1])
            return False
        
        elif no[0] == "TIPO":
            self.tipo(no[1])
            return False
        
        elif no[0] == 'VARIAVEL':
            self.variavel(no[1])
            return False
        
        elif no[0] == "NOME_ROTINA":
            self.nome_rotina(no[1])
            return False
        
        # Preciso tratar nomes
        # Existem nomes em: COMANDOS(ATRIB e READ), NOME e PARAMETRO
        # Tratar cada tipo de nome (Chamada de função, campo de registro e acesso em array)
        elif no[0] == "COMANDO":
            #print(no)
            if no[1][0][0] == "READ":
                no_nome = no[1][2]
                identificador = no[1][1][1]
                self.nome(identificador, no_nome)
            
            elif no[1][0][0] == "ID": 

                if no[1][2] != None: # Atribuição

                    # ('COMANDO', (('ID', 'i', 40), None, ('ATRIB', (('ATRIBUICAO', ':=', 40), ('EXP_MAT', ('PARAMETRO', ('NUMERO', '1', 40)))))))
                    #print(no[1])
                    # Termo a esquerda
                    id_esq = no[1][0][1]
                    if no[1][1] == None:
                        simbolo_esq = self.Tabela.lookup(id_esq, self.escopo) # Checar se existe na tabela
                        if simbolo_esq == None:
                            printv(f"ERRO: {id_esq} não foi declarado!")
                            return False
                        
                        tipo_esq = simbolo_esq[2]
                    else: # Caso tenha nome
                        pass

                    no_dir = no[1][2][1][1][1]
                    #print(no_dir)
                    
                    tipo_dir = None
                    if no_dir[1][0] == "NUMERO":
                        tipo_dir = "INTEGER"
                        if "." in no_dir[1][1]:
                            tipo_dir = "REAL"
                    
                    else: # Tratar nome
                        if no_dir[0] == "PARAMETRO": # função
                            id_dir = no_dir[1][0][1]
                            simbolo_id = self.Tabela.lookup(id_dir, self.escopo)

                            if simbolo_id == None:
                                printv(f"ERRO: {id_dir} não foi declarado!")
                                return False
                            
                            if no_dir[1][1] == None:
                                tipo_dir = simbolo_id[2]
                            
                            else: #Nome
                                no_nome = no_dir[1][1]
                                tipo_dir = self.nome(id_dir, no_nome)
                            
                        
                        else:
                            id_dir = no_dir[0][1][0][1]

                            if no_dir[0][1][1] == None: # Sem nome
                                simbolo_id = self.Tabela.lookup(id_dir, self.escopo)

                                if simbolo_id == None:
                                    printv(f"ERRO: {id_dir} não foi declarado!")
                                    return False
                                
                                tipo_dir = simbolo_id[2]

                                if simbolo_id[2] == "NUMERO":
                                    tipo_dir = "INTEGER"
                        
                            
                            else: # Com nome
                                simbolo_id = self.Tabela.lookup(id_dir, self.escopo)

                                if simbolo_id == None:
                                    printv(f"ERRO: {id_dir} não foi declarado!")
                                    return False
                                
                                no_nome = no_dir[0][1][1]
                                tipo_dir = self.nome(id_dir, no_nome)
                        
                        if tipo_dir != tipo_esq:
                                printv(f"ERRO: Tipo de {id_esq}:{tipo_esq} diferente de {id_dir}:{tipo_dir}")
                                return False

                    

            
                else: #Chamada de função
                    id_func = no[1][0][1]
                    no_nome = no[1][1]
                    simbolo_func = self.Tabela.lookup(id_func, self.escopo)

                    if simbolo_func == None:
                        printv(f"ERRO: {no[1]} não foi declarado!")
                        return False
                    
                    if simbolo_func[1] == "FUNCTION":
                        self.nome(id_func, no_nome)



            return False

        elif no[0] == 'ID': # Verifica se o ID existe na tabela
            # Lidar com variaveis record
            if self.Tabela.lookup(no[1], self.escopo) == None:
                printv(f"ERRO: {no} não foi declarado!")
            return False

        else:
            return True
 
    def constante(self, no):
        # nome, CONSTANTE, CONSTANTE, escopo, None, None 
        if no[2][1][0] == "EXP_MAT":
            simbolo = (no[0][1], 'CONSTANTE', 'NUMERO', self.escopo, None, None) 
        else:
            simbolo = (no[0][1], 'CONSTANTE', 'STRING', self.escopo, None, None) 

        self.Tabela.add(simbolo)
    
    def tipo(self, no):
        # nome, TIPO, tipo, escopo, qtd, NONE 
        tipo_tipo = self.tipo_dado(no[2])
        simbolo = (no[0][1], "TIPO", tipo_tipo[0], self.escopo, tipo_tipo[1], None)
        self.Tabela.add(simbolo)

    def variavel(self, no):
        # nome, VARIAVEL, tipo, escopo, qtd, None 
        var_tipo = self.tipo_dado(no[3])
        if no[1] == None: # Variavel sozinha
            simbolo = (no[0][1], "VARIAVEL", var_tipo[0], self.escopo, var_tipo[1], None)
            self.Tabela.add(simbolo)
        
        else: 
            self.Tabela.add((no[0][1], "VARIAVEL", var_tipo[0], self.escopo, var_tipo[1], None))

            lista_id = no[1][1]
            self.Tabela.add((lista_id[1][1], "VARIAVEL", var_tipo[0], self.escopo, var_tipo[1], None))
            while lista_id[2] != None:
                lista_id = lista_id[2][1]
                self.Tabela.add((lista_id[1][1], "VARIAVEL", var_tipo[0], self.escopo, var_tipo[1], None))

    def param_rot(self, no):
        # nome, PARAMETRO, tipo, escopo, qtd, ordem 
        ordem = 1
        campos = no[1][1]
        param_tipo = self.tipo_dado(campos[2])
        simbolos_param = [(campos[0][1], "PARAMETRO", param_tipo[0], self.escopo, param_tipo[1], ordem)]
        self.Tabela.add(simbolos_param[0])
        
        while campos[3] != None:
            ordem += 1
            campos = campos[3][1][1][1]
            param_tipo = self.tipo_dado(campos[2])
            simbolos_param.append((campos[0][1], "PARAMETRO", param_tipo[0], self.escopo, param_tipo[1], ordem))
            self.Tabela.add(simbolos_param[ordem-1])
        
        return simbolos_param

    def nome_rotina(self, no):
        if no[0][0] == "PROCEDURE":
            self.Tabela.add((no[1][1], "PROCEDURE", None, "GLOBAL", None, None))
        
        elif no[0][0] == "FUNCTION":
            # nome, TIPO, tipo, escopo, qtd, parametros 
            func_tipo = self.tipo_dado(no[4])
            parametros = self.param_rot(no[2][1])
            self.Tabela.add((no[1][1], "FUNCTION", func_tipo[0], "GLOBAL", func_tipo[1], parametros))
    
    def nome_ponto(self, ID, no_nome):
        simbolo = self.Tabela.lookup(ID, self.escopo)

        if simbolo == None: # Verificar se o ID existe 
            printv(f"ERRO: {ID} não foi declarado!")
            return None
        
        # Verificar se o tipo do ID corresponde a um record existente
        tipo = simbolo[2]
        record = self.Tabela.lookup(tipo, self.escopo)

        if record == None or record[2] != "RECORD":
            printv(f"ERRO: {ID} é {simbolo[2]} não um RECORD!")
            return None
        
        campo_nome = no_nome[1][1][1]
        campos = record[4]

        existe_campo = False
        tipo_campo = None
        for campo in campos:
            if campo_nome == campo[0]:
                existe_campo = True
                tipo_campo = campo[2]
                break
        
        if not existe_campo:
            printv(f"ERRO: não existe {campo_nome} em {tipo}!")
            return None
        
        return tipo_campo
    
    def nome_colchete(self, ID, no_nome):
        simbolo_id = self.Tabela.lookup(ID, self.escopo)

        if simbolo_id == None:
            printv(f"ERRO: {ID} Não foi declarado")
            return None

        tipo = simbolo_id[2]

        # (Nome, Classificação, Tipo, Escopo, Quantidade, Ordem)
        simbolo_type = self.Tabela.lookup(tipo, self.escopo)
        if simbolo_type == None: # ID é um integer ou real
            simbolo = simbolo_id
        else:
            simbolo = simbolo_type

        if simbolo[4] != None: # ID é um array
            tamanho_array = int(simbolo[4])
            id_index = int(no_nome[1][1][1][1]) # Tratar para o caso de ID
            if id_index > tamanho_array or id_index < 1:
                printv(f"ERRO: index não corresponde ao tamanho do array {simbolo_id[0]}")
                return None
        
        else:
            printv(f"ERRO: {simbolo_id[0]} não é um array")
            return None

        return simbolo[2]
    
    def conta_param(self, no, valor):
        contador = 0
        if no[0] == valor:
            return 1
        
        else:
            for filho in no:
                if isinstance(filho, tuple):
                    contador += self.conta_param(filho, valor)

        return contador

    def nome_parentesis(self, ID, no_nome):
        # Checar se é função
        # Ver se todos os parametros foram passados 
        # Ver se os parametros correspondem aos tipos, caso seja um ID
        simbolo_id = self.Tabela.lookup(ID, self.escopo)

        if simbolo_id == None:
            printv(f"ERRO: {ID} Não foi declarado")
            return None
        
        if simbolo_id[1] != "FUNCTION":
            printv(f"ERRO: {ID} Não é uma função")
            return None
        
        tipo = simbolo_id[2]
        
        parametros_id = simbolo_id[5]
        lista_params = no_nome[1][1]

        num_parametros = self.conta_param(lista_params, "PARAMETRO")

        if num_parametros != len(parametros_id):
            printv(f"ERRO: função {ID} recebeu {num_parametros} parametros mas suporta apenas {len(parametros_id)}")
            return tipo

        parametros_declarados = []

        for i in range(num_parametros-1):
            param = lista_params[1][0][1]
            parametros_declarados.append(param)
            lista_params = lista_params[1][2]

        param = lista_params[1][1]
        parametros_declarados.append(param)

        for i in range(len(parametros_declarados)):
            if parametros_declarados[i][0] == "NUMERO":
                if parametros_id[i][2] != "REAL" and parametros_id[i][2] != "INTEGER":
                    printv(f"ERRO: O parametro {i+1} de {simbolo_id[0]} esperado é um {parametros_id[i][2]} ")
            
            else:
                simbolo_param = self.Tabela.lookup(parametros_declarados[i][0][1], self.escopo)
                if simbolo_param == None:
                    printv(f"ERRO: O ID {parametros_declarados[i][0][1]} não foi declarado!")
                
                else:
                    if simbolo_param[2] == "NUMERO":
                        if parametros_id[i][2] != "REAL" and parametros_id[i][2] != "INTEGER":
                            printv(f"ERRO: O parametro {i+1} de {simbolo_id[0]} esperado é um {parametros_id[i][2]} mas foi recebido {simbolo_param[i][2]}")
                    
                    elif simbolo_param[2] != parametros_id[i][2]:
                        printv(f"ERRO: O parametro {i+1} de {simbolo_id[0]} esperado é um {parametros_id[i][2]} mas foi recebido {simbolo_param[2]}")


        return tipo

    def nome(self, ID, no_nome): # Retorna o tipo do nome 
        if no_nome[1][0][0] == "PONTO": #Pertence a um record
            return self.nome_ponto(ID, no_nome)
        
        elif no_nome[1][0][0] == "COLCHETE_ESQ": # Array
            return self.nome_colchete(ID, no_nome)
        
        elif no_nome[1][0][0] == "PARENTESIS_ESQ":
            return self.nome_parentesis(ID, no_nome)
            
    def record(self, no):
        campos = no[1][1][1][1]

        simbolos_campos = []
        tipo_record = self.tipo_dado(campos[2])
        simbolos_campos.append((campos[0][1], 'CAMPO', tipo_record[0], self.escopo, tipo_record[1], None))

        prox_campo = campos
        while prox_campo[3] != None:
            prox_campo = prox_campo[3][1][1][1]
            tipo_record = self.tipo_dado(prox_campo[2])
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
