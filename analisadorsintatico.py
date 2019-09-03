from analisadorlexico import AnalisadorLexico


class Variavel:

    def __init__(self, representacao):
        self.representacao = representacao


    def __str__(self):
        return self.representacao


    def __repr__(self):
        return self.__str__()


class Terminal:
    
    def __init__(self, representacao):
        self.representacao = representacao


    def __str__(self):
        return self.representacao


    def __repr__(self):
        return self.__str__()


class RegraProducao:

    def __init__(self, regraInicial, regrasGeradas):
        self.regraInicial  = regraInicial
        self.regrasGeradas = regrasGeradas      


    def __str__(self):
        return ("%s --> %s" % (self.regraInicial, self.regrasGeradas))


    def __repr__(self):
        return self.__str__()


class AnalisadorSintatico:

    def __init__(self):
        self.tabelaTransicao = {}
        self.pilha = []

    
    def construirTabelaTransicao(self):
        tabelaTransicao = self.tabelaTransicao

        # Define as Variaveis utilizadas pelas transicoes
        E = Variavel('E')
        T = Variavel('T')
        S = Variavel('S')
        F = Variavel('F')
        G = Variavel('G')

        # Define os terminais utilizados
        add   = Terminal('+')
        sub   = Terminal('-')
        _id   = Terminal('id')
        num   = Terminal('num')
        mult  = Terminal('*')
        div   = Terminal('/')
        void  = Terminal('\'')
        abre  = Terminal('(')
        fecha = Terminal(')')
        vazio = Terminal('$')


        # Define as regras de producao
        regra1 = RegraProducao(E, [T, S])
        regra2 = RegraProducao(T, [F, G])        
        regra3 = RegraProducao(S, [add, T, S])
        regra4 = RegraProducao(S, [sub, T, S])
        regra5 = RegraProducao(S, [void])
        regra6 = RegraProducao(G, [void])
        regra7 = RegraProducao(G, [mult, F, G])
        regra8 = RegraProducao(G, [div, F, G])
        regra9 = RegraProducao(F, [_id])
        regra10 = RegraProducao(F, [num])
        regra11 = RegraProducao(F, [abre, E, fecha])

        # Monta a tabela em si
        tabelaTransicao[E] = {}
        tabelaTransicao[E][_id] = regra1
        tabelaTransicao[E][num] = regra2
        tabelaTransicao[E][abre] = regra1

        tabelaTransicao[T] = {}
        tabelaTransicao[T][_id] = regra2
        tabelaTransicao[T][num] = regra2
        tabelaTransicao[T][abre] = regra2

        tabelaTransicao[S] = {}
        tabelaTransicao[S][add] = regra3
        tabelaTransicao[S][sub] = regra4
        tabelaTransicao[S][fecha] = regra5
        tabelaTransicao[S][vazio] = regra5

        tabelaTransicao[G] = {}
        tabelaTransicao[G][add] = regra6
        tabelaTransicao[G][sub] = regra6
        tabelaTransicao[G][mult] = regra7
        tabelaTransicao[G][mult] = regra8
        tabelaTransicao[G][fecha] = regra6
        tabelaTransicao[G][vazio] = regra6

        tabelaTransicao[F] = {}
        tabelaTransicao[F][_id] = regra9
        tabelaTransicao[F][num] = regra10
        tabelaTransicao[F][abre] = regra11


    def extrairTokens(self, arquivo):

        analisador = AnalisadorLexico()
        analisador.carregaListaCaracteresEspeciais("specialTokens.json")
        analisador.carregaListaPalavrasChave("keywords.json")
        analisador.carregaArquivoCompilar(arquivo)
        analisador.constroiAutomato()
        analisador.parsearTokens()
        
        self.fluxoTokens = analisador.listaTokens


    def analisar(self):
        self.extrairTokens("samples/input.txt")

        tabelaSolucao = list()
        pilha = list()
        cadeia = self.fluxoTokens
        regra = None

        # inicio algoritmo
        pilha.append()





    


analisador = AnalisadorSintatico()
analisador.construirTabelaTransicao()   
analisador.analisar()
