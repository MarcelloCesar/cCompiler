from analisadorlexico import AnalisadorLexico, Token
import tabulate

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

    
    def copy(self):
        return RegraProducao(
            self.regraInicial,
            self.regrasGeradas
        )


class AnalisadorSintatico:

    def __init__(self):
        self.tabelaTransicao = {}

    
    def construirTabelaTransicao(self):
        tabelaTransicao = self.tabelaTransicao

        # Define as Variaveis utilizadas pelas transicoes
        self.variaveis = {}

        E = Variavel('E')
        self.variaveis[E] = E
        self.variavelInicial = E

        T = Variavel('T')
        self.variaveis[T] = T

        S = Variavel('S')
        self.variaveis[S] = S

        F = Variavel('F')
        self.variaveis[F] = F

        G = Variavel('G')
        self.variaveis[G] = G

        # Define os terminais utilizados
        add   = Terminal('+')
        sub   = Terminal('-')
        id    = Terminal('id')
        num   = Terminal('num')
        mult  = Terminal('*')
        div   = Terminal('/')
        vazio  = Terminal('\'')
        abre  = Terminal('(')
        fecha = Terminal(')')
        vazio = Terminal('$')


        # Define as regras de producao
        self.regrasProducao = {}
        regra1 = RegraProducao(E, [T, S])
        self.producaoInicial = regra1

        regra2 = RegraProducao(T, [F, G])        
        regra3 = RegraProducao(S, [add, T, S])
        regra4 = RegraProducao(S, [sub, T, S])
        regra5 = RegraProducao(S, [vazio])
        regra6 = RegraProducao(G, [vazio])
        regra7 = RegraProducao(G, [mult, F, G])
        regra8 = RegraProducao(G, [div, F, G])
        regra9 = RegraProducao(F, [id])
        regra10 = RegraProducao(F, [num])
        regra11 = RegraProducao(F, [abre, E, fecha])

        # Monta a tabela em si
        tabelaTransicao[E] = {}
        tabelaTransicao[E][id.__str__()] = regra1
        tabelaTransicao[E][num.__str__()] = regra2
        tabelaTransicao[E][abre.__str__()] = regra1

        tabelaTransicao[T] = {}
        tabelaTransicao[T][id.__str__()] = regra2
        tabelaTransicao[T][num.__str__()] = regra2
        tabelaTransicao[T][abre.__str__()] = regra2

        tabelaTransicao[S] = {}
        tabelaTransicao[S][add.__str__()] = regra3
        tabelaTransicao[S][sub.__str__()] = regra4
        tabelaTransicao[S][fecha.__str__()] = regra5
        tabelaTransicao[S][vazio.__str__()] = regra5

        tabelaTransicao[G] = {}
        tabelaTransicao[G][add.__str__()] = regra6
        tabelaTransicao[G][sub.__str__()] = regra6
        tabelaTransicao[G][mult.__str__()] = regra7
        tabelaTransicao[G][div.__str__()] = regra8
        tabelaTransicao[G][fecha.__str__()] = regra6
        tabelaTransicao[G][vazio.__str__()] = regra6

        tabelaTransicao[F] = {}
        tabelaTransicao[F][id.__str__()] = regra9
        tabelaTransicao[F][num.__str__()] = regra10
        tabelaTransicao[F][abre.__str__()] = regra11

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

        self.fluxoTokens.append(Terminal('$'))

        self.solucao = []
        self.pilha   = ['$', self.variavelInicial]
        self.producaoAtual = self.producaoInicial        

        # Adiciona a linha da solicao inicial
        self.adicionaSolucao()
        # inicio algoritmo
        while self.fluxoTokens.__len__() > 1 or self.pilha.__len__() > 1:  
            try:                      
                if type(self.pilha[-1]) == Terminal and str(self.pilha[-1]) == str(self.pilha[-1]):#Rever isso, e se for uma variavel E no fonte em C? v- ver se colocando Terminal como coloquei ja resolve
                    # consome a pilha e o token                
                    if self.pilha.__len__() > 1:
                        self.pilha.pop()

                    if self.fluxoTokens.__len__() > 1:                
                        self.fluxoTokens.pop(0)

                    self.producaoAtual = '----'

                else:                    
                    self.producaoAtual = self.tabelaTransicao[self.pilha[-1]][str(self.fluxoTokens[0])].copy()
                    producaoAdicionarPilha = self.producaoAtual.regrasGeradas.copy()
                    producaoAdicionarPilha.reverse()
                        
                    self.pilha.pop()

                    for regra in producaoAdicionarPilha:
                        if regra not in self.pilha and \
                           regra.__str__() != '$':
                            self.pilha.append(regra)  


                self.adicionaSolucao()
            except Exception as exc:
                raise exc

        self.printaSolucao()
                
    
    def adicionaSolucao(self):
        self.solucao.append([
            self.pilha.copy(),
            self.fluxoTokens.copy(),
            self.producaoAtual
        ])

    
    def printaSolucao(self):
        for i in range(self.solucao.__len__()):
            try:
                self.solucao[i][-1] = self.solucao[i+1][-1]
            except:
                pass

        print(tabulate.tabulate(self.solucao, headers=["Pilha", "Cadeia", "Regra"]))


if __name__ == '__main__':
    analisador = AnalisadorSintatico()
    analisador.construirTabelaTransicao()   
    analisador.analisar()

