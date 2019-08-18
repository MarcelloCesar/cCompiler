import re
import json
class Estado:

    def __init__(self, nomeEstado, final=False):
        self.nome  = nomeEstado
        self.final = final

    def __eq__(self, estado):

        if self.nome == estado.nome:
            return True
        
        return False


    def __str__(self):
        return self.nome
    
    def gerarTransicao(self, estado, charConsumir, acao=None):
        return Transicao(self, estado, charConsumir, acao)


class Transicao:

    def __init__(self, estadoInicial, estadoFinal, charConsumir, acao=None):
        self.estadoInicial = estadoInicial
        self.estadoFinal   = estadoFinal
        self.charConsumir  = charConsumir
        self.acao          = acao

    
    def __eq__(self, transicao):
        if self.estadoInicial == transicao.estadoInicial and \
           self.estadoFinal   == transicao.estadoFinal   and \
           self.charConsumir  == transicao.charConsumir:
           return True

        return False    

    def __str__(self):
        return str(tuple(
            (str(self.estadoInicial),
             str(self.estadoFinal),
             str(self.charConsumir))
        ))


class Automato:

    def __init__(self):
        self.listaEstados     = list()
        self.listaTransicoes  = list()        
        self.estadoAtual = None


    def adicionaEstado(self, estado):
        if estado not in self.listaEstados:
            self.__dict__["estado_" + estado.nome] = estado
            self.listaEstados.append(estado)
            estado.listaTransicoesNoGrafo = list()


    def adicionaTransicao(self, transicao):
        if transicao not in self.listaTransicoes:

            if transicao.estadoInicial not in self.listaEstados or \
               transicao.estadoFinal   not in self.listaEstados:
               raise Exception("Não foi possivel adicionar transicao pois um dos estados desta transicao nao existe no automato") 
            
            self.listaTransicoes.append(transicao)
            transicao.estadoInicial.listaTransicoesNoGrafo.append(
                transicao
            )


    def defineEstadoInicial(self, estado):
        if(estado not in self.listaEstados):
            raise Exception("Impossível setar como inicial estado nao existente no automato")

        self.estadoInicial = estado


    def reinicializar(self):
        if('estadoInicial' not in self.__dict__):
            raise Exception("Impossível inicializar automato sem definir estado inicial")

        self.estadoAtual = self.estadoInicial

    
    def consomeChar(self, caracter):
        #print('-----')
        #for i in self.estadoAtual.listaTransicoesNoGrafo:
         #   print(i, end=", ")
          #  print()
        for transicao in self.estadoAtual.listaTransicoesNoGrafo:
            if re.search(transicao.charConsumir, caracter):
                self.estadoAtual = transicao.estadoFinal
                if transicao.acao:
                    transicao.acao()
                return

        raise Exception(
            "Transicao inexistente para o caracter informado. " + 
            "Estado Atual: " + str(self.estadoAtual) + 
            ". Caracter Lido: '" + caracter + "', #" + str(ord(caracter)) + "."
        )

    
class AnalisadorLexico:

    def __init__(self):
        pass


    def carregaListaCaracteresEspeciais(self, path):    
        with open(path, "r") as file:
            self.listaCaracteresEspeciais = json.load(file)

    
    def carregaListaPalavrasChave(self, path):
        with open(path, "r") as file:
            self.listaPalavrasChave = json.load(file)

    
    def carregaArquivoCompilar(self, path):
        with open(path, "r") as file:
            conteudo = file.read()
            conteudo = conteudo.replace("\r", " ")
            conteudo = conteudo.replace("\n", " ")
            conteudo = conteudo.replace(chr(9), " ")
            self.conteudoCompilar = conteudo


    def constroiAutomato(self):
        automato = Automato()

        automato.adicionaEstado(Estado('1'))
        automato.adicionaEstado(Estado('2'))
        automato.adicionaEstado(Estado('3'))
        automato.adicionaEstado(Estado('4'))
        automato.adicionaEstado(Estado('5'))

        automato.adicionaTransicao(
            automato.estado_1.gerarTransicao(
                automato.estado_2, 
                '[a-zA-Z_]',
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_1.gerarTransicao(
                automato.estado_1, 
                '[ ]'
            )
        )

        automato.adicionaTransicao(
            automato.estado_1.gerarTransicao(
                automato.estado_1, 
                "[" + "".join(self.listaCaracteresEspeciais) + "]",
                self.criarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_1.gerarTransicao(
                automato.estado_3, 
                "[0-9]",
                self.incrementarToken
            )
        )
        
        automato.adicionaTransicao(
            automato.estado_2.gerarTransicao(
                automato.estado_1, 
                ' ',
                self.finalizarToken
            )
        )
        
        automato.adicionaTransicao(
            automato.estado_2.gerarTransicao(
                automato.estado_1,
                "[" + "".join(self.listaCaracteresEspeciais) + "]",
                self.finalizarTokenCriarToken         
            )
        )

        automato.adicionaTransicao(
            automato.estado_2.gerarTransicao(
                automato.estado_1,
                "[.]",
                self.finalizarTokenCriarToken         
            )
        )

        automato.adicionaTransicao(
            automato.estado_2.gerarTransicao(
                automato.estado_2,
                "[a-zA-Z0-9_]",
                self.incrementarToken         
            )
        )

        automato.adicionaTransicao(
            automato.estado_3.gerarTransicao(
                automato.estado_1,
                "[" + "".join(self.listaCaracteresEspeciais) + "]",
                self.finalizarTokenCriarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_3.gerarTransicao(
                automato.estado_1,
                "[ ]",
                self.finalizarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_3.gerarTransicao(
                automato.estado_3,
                "[0-9]",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_3.gerarTransicao(
                automato.estado_5,
                "[.]",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_3.gerarTransicao(
                automato.estado_4,
                "[a-z]",
                self.erroLexico
            )
        )  

        automato.adicionaTransicao(
            automato.estado_4.gerarTransicao(
                automato.estado_4,
                "[a-z]"
            )
        )

        automato.adicionaTransicao(
            automato.estado_4.gerarTransicao(
                automato.estado_1,
                "[" + "".join(self.listaCaracteresEspeciais) + "]"
            )
        )

        automato.adicionaTransicao(
            automato.estado_5.gerarTransicao(
                automato.estado_5,
                "[0-9]",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_5.gerarTransicao(
                automato.estado_1,
                "[" + "".join(self.listaCaracteresEspeciais) + "]",
                self.finalizarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_5.gerarTransicao(
                automato.estado_4,
                "[a-zA-Z]",
                self.erroLexico
            )
        )
        
        automato.defineEstadoInicial(automato.estado_1)
        automato.reinicializar()
        self.automato = automato

    
    def lerCaracter(self, caracter):
        self.automato.consomeChar(caracter)

    
    def parsearTokens(self):
        self.stringTokenAtual = ''
        self.listaTokens      = list()        
        for caracter in self.conteudoCompilar:
            self.charLidoAtual = caracter
            self.lerCaracter(caracter)


    
    def incrementarToken(self):
        self.stringTokenAtual += self.charLidoAtual

    
    def finalizarToken(self):
        self.listaTokens.append(self.stringTokenAtual)        
        self.stringTokenAtual = ''
        

    def criarToken(self):
        self.incrementarToken()
        self.finalizarToken()


    def finalizarTokenCriarToken(self):
        self.finalizarToken()
        self.criarToken()


    def erroLexico(self):
        raise Exception("Caracter inexperado: ", self.charLidoAtual)


if __name__ == "__main__":
    analisador = AnalisadorLexico()
    analisador.carregaListaCaracteresEspeciais("specialTokens.json")
    analisador.carregaListaPalavrasChave("keywords.json")
    #analisador.carregaArquivoCompilar("samples/Jogo de Boca.cpp")
    analisador.carregaArquivoCompilar("samples/program.c")
    #analisador.carregaArquivoCompilar("samples/Cliente.java")
    analisador.constroiAutomato()
    analisador.parsearTokens()
    print(analisador.listaTokens)

# Todo: Tratar Aspas e Strings
# Todo: Tratar comentarios
# tratar numero linha e coluna