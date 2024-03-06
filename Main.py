def ler_dfa():
    while(True):
        var = input("Informe o nome do arquivo .txt que contem a tabela de transição do DFA. Exemplo(dfa.txt):")
        try:
            with open(var, "r") as arquivo:
                tabela = arquivo.readlines()
            # print(tabela)
            break
        except:
            print("ERRO arquivo nao existe")

    #qtd_estados = (len(tabela) - 1)

    # coleta os simbolos
    simbolos = tabela[0]
    simbolos_dfa = simbolos.split()
    qtd_simbolos = (len(simbolos_dfa))
    # ---------------------

    # coleta as linhas onde estao as transicoes
    linhas = []
    for i in range(1, len(tabela)):
        linhas.append(tabela[i].split())
    # ------------------------------------

    verifica_estado = []
    for char in linhas:
        verifica_estado.append(char[0])
    # coletar o inicial
    for estado in verifica_estado:
        if '>' in estado:
            estado_inicial_DFA = estado.replace('>', '')
            estado_inicial_DFA = estado_inicial_DFA.replace('*', '')

    # -------------------------------

    # coletar os estados finais
    estado_final_DFA = []
    for estado in verifica_estado:
        if '*' in estado:
            aux = estado.replace('*', '')
            estado_final_DFA.append(aux.replace('>', ''))



    # Coleta o nome dos estados
    estados_dfa = []
    for char in linhas:
        aux = char[0].replace('>', '')
        aux = aux.replace('*', '')
        estados_dfa.append(aux)
        del char[0]  # remove esses elementos da tabela

    transacao_dfa = linhas

    print("Estados Iniciais DFA")
    print(estado_inicial_DFA)

    print("Simbolos DFA")
    print(simbolos_dfa)

    print("Estados DFA")
    print(estados_dfa)

    print("Transacao do DFA")
    print (transacao_dfa)

    print("Estados Finais DFA")
    print(estado_final_DFA)
    return (estados_dfa, estado_inicial_DFA, estado_final_DFA, simbolos_dfa, transacao_dfa)


def e_nfa_dfa():#le o arquivo contendo o NFA ou e-NFA e converte para DFA
    while (True):
        var = input("Informe o nome do arquivo .txt que contem a tabela de transição do e-NFA ou  NFA. Exemplo(nfa.txt):")
        try:
            with open(var, "r") as arquivo:
                tabela = arquivo.readlines()
            #print(tabela)
            break
        except:
            print("ERRO arquivo nao existe")


    qtd_estados = (len(tabela)-1)

    #coleta os simbolos
    simbolos_arquivo = tabela[0]
    simbolos = simbolos_arquivo.split()
    qtd_simbolos = (len(simbolos))
    #print("Simbolos:")
    #print(simbolos)
    #---------------------

    #coleta as linhas onde estao as transicoes
    linhas = []
    for i in range(1, len(tabela)):
        linhas.append( tabela[i].split())
    #------------------------------------

    #print(linha)
    verifica_estado = []
    for char in linhas:
        verifica_estado.append(char[0])
    #coletar o inicial
    for estado in verifica_estado:
        if '>' in estado:
            estado_inicial = estado.replace('>','')
            estado_inicial = estado_inicial.replace('*', '')

    #print("Estado inicial: "+estado_inicial)
    #-------------------------------

    #coletar os estados finais
    estado_final = []
    for estado in verifica_estado:
        if '*' in estado:
            aux = estado.replace('*','')
            estado_final.append( aux.replace('>', ''))

    #print("Estados Finais: ")
    #print(estado_final)

    #Coleta o nome dos estados
    s = []
    for char in linhas:
        aux = char[0].replace('>','')
        aux = aux.replace('*','')
        s.append(aux)
        del char[0]#remove esses elementos da tabela
    #print("Estados do automato: ")
    #print(s)
    #
    transacoes = {}
    for i in range(len(linhas)):
        #print(linhas[i])
        transacoes[i] = {}
        for j in range(len(linhas[i])):
            #print(linhas[i][j])
            aux = linhas[i][j].replace('{', '')
            aux = aux.replace('}', '')
            aux = aux.split(',')
            #print(aux)
            transacoes[i][j] = aux
            for k in range(len(linhas[i][j])):
                #print(linhas[i][j][k])
                aux = linhas[i][j][k].replace('{','')
                aux = aux.replace('}','')
                #print(aux)
    #print("Transações NFA")
    #print(transacoes)

    #COMECA A CONVERSAO
    estados_dfa = []

    def e_closure_inicial(estado):
        e_cl = []
        e_cl.append(estado)
        estados_dfa.append(e_closure([estado]))

    def e_closure(estado):#s.index(p) coleta a posicao do vetor que corresponde àquele determinado estado
        e_cl = []
        e_cl = e_cl + estado
        for p in estado:
            #simbolos.index('&') coletaa posicao do vetor que corresponde àquele determinado simbolo
            if '&' in simbolos:#verifica se trata de um ENFA
                for e in transacoes[s.index(p)][simbolos.index('&')]:# coleta os estados alcançados por p atraves do vazio
                    if len(e) > 0:
                        if e not in e_cl:#verifica se esse estado ja n foi computado
                            e_cl.append(e)
        if estado == e_cl:#se não foi adicionado mais nenhum estado retorna a lista
            return e_cl

        return e_closure(e_cl) #enquanto novos estados forem adicionados chamar a função para esses novos estados

    def move(estados,simbol):
        novo_estado = []
        for est in estados:
            for e in transacoes[s.index(est)][simbolos.index(simbol)]:# coleta os estados alcançados por p atraves do vazio
                if len(e) > 0:
                    if e not in novo_estado:#verifica se esse estado ja n foi computado
                        novo_estado.append(e)
        return novo_estado

    e_closure_inicial(estado_inicial)
    estado_inicial_DFA = estados_dfa[0]
    transacao_dfa = {}
    simbolos_dfa = simbolos.copy()
    if '&' in simbolos_dfa:#verifica se trata de um ENFA
        simbolos_dfa.remove('&')
    i=0
    j=0
    for estado in estados_dfa:
        transacao_dfa[i] = {}
        j=0
        for simbol in simbolos_dfa:
            aux = e_closure(move(estado, simbol))
            if aux not in estados_dfa:
                estados_dfa.append(aux)
            transacao_dfa[i][j] = aux
            j += 1
        i += 1

    #definir estados finais
    estado_final_DFA = []

    for estado in estados_dfa:
        for estado_f in estado_final:
            if estado_f in estado and estado not in estado_final_DFA:
                estado_final_DFA.append(estado)


    print("Estados Iniciais DFA")
    print(estado_inicial_DFA)

    print("Simbolos DFA")
    print(simbolos_dfa)

    print("Estados DFA")
    print(estados_dfa)

    print("Transacao do DFA")
    print (transacao_dfa)

    print("Estados Finais DFA")
    print(estado_final_DFA)
    return (estados_dfa,estado_inicial_DFA,estado_final_DFA,simbolos_dfa,transacao_dfa)


def convert(p,q,transacao_dfa,simbolos_dfa,estados_dfa):
    return transacao_dfa[estados_dfa.index(p)][simbolos_dfa.index(q)]

def verifica_string(estados_dfa,estado_inicial_DFA,estado_final_DFA,simbolos_dfa,transacao_dfa):
    aceita = 0#variavel para verificar se a linguagem aceita a string

    #Le o arquivo que contem as strings que serao testadas
    while (True):
        var = input("Informe o nome do arquivo .txt que contem as strings que serão testadas pelo autômato. Exemplo(string.txt):")
        try:
            with open(var, "r") as arquivo:
                dados = arquivo.readlines()
            break
        except:
            print("ERRO arquivo nao existe")

    #coloca as strings do arquivo em uma lista
    strings = []
    for i in range(1, len(dados)):
        strings.append( dados[i].split())
    print("Strings para leitura: ")
    print(strings)
    #---------------------------------------------
    resultado = []
    for i in range(len(strings)):
        for a in strings[i]:
            q =a
        print("String:")
        print (q)
        li=[]#armazena a sequencia de estados que a string percorreu
        start = estado_inicial_DFA
        for j in q:
            start=convert(start,j,transacao_dfa,simbolos_dfa,estados_dfa)
            li.append(start)#adiciona na lista o estado atingido depois de ler determinado caracter da string

        for final in estado_final_DFA:
            if (li[-1] == final):
                aceita = 1
        if(aceita == 1):#-1 representa o ultimo elemento da lista
            print("Sim")
            resultado.append(q+" *\n")
            print(li)
        else:
            print("Não")
            resultado.append(q+"\n")
            print("sequencia de estados atingidos:")
            print(li)
        aceita = 0

    try:
        with open("resultado.txt", "w") as arquivo:
                arquivo.writelines(resultado)
    except:
        print("ERRO arquivo nao existe")

def nfa():
    (estados_dfa, estado_inicial_DFA, estado_final_DFA, simbolos_dfa, transacao_dfa) = e_nfa_dfa()
    verifica_string(estados_dfa, estado_inicial_DFA, estado_final_DFA, simbolos_dfa, transacao_dfa)

def dfa():
    (estados_dfa, estado_inicial_DFA, estado_final_DFA, simbolos_dfa, transacao_dfa) = ler_dfa()
    verifica_string(estados_dfa, estado_inicial_DFA, estado_final_DFA, simbolos_dfa, transacao_dfa)

def menu():
    var = None
    while var != 3:
        if var == 1:
            dfa()
            break
        if var == 2:
            nfa()
            break
        print("1 - Ler e Calcular DFA")
        print("2 - Ler e Calcular NFA ou E-NFA")
        print("3 - Sair")
        var = int(input("Insira a opção: "))
menu()