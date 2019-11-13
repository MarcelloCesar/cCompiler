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

class Token:

    def __init__(self, valor, tipoToken, linha):
        self.valor = valor
        self.tipo  = tipoToken
        self.linha = linha


    def __str__(self):
        return self.valor
        return "<" + self.valor + ', ' + self.tipo + ">\n"


    def __eq__(self, token):
        return str(token) == self.__str__()


    def __repr__(self):
        return self.__str__()


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
            linhasArquivo = file.readlines()
            linhas = list()
            for linha in linhasArquivo:
                if (linha.strip().__len__() > 0 and \
                   linha.strip()[0] == '#') or \
                   (linha.strip().__len__() > 1 and linha.strip()[0] == '/' and linha.strip()[1] == '/'):
                    pass
                else:
                    linhas.append(linha)
                #print(str(linhas) + "\n\n\n\n\n")
            self.linhasArquivoCompilar = linhas


    def constroiAutomato(self):
        automato = Automato()

        automato.adicionaEstado(Estado('1'))
        automato.adicionaEstado(Estado('2'))
        automato.adicionaEstado(Estado('3'))
        automato.adicionaEstado(Estado('4'))
        automato.adicionaEstado(Estado('5'))
        automato.adicionaEstado(Estado('6'))
        automato.adicionaEstado(Estado('7'))

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
            automato.estado_1.gerarTransicao(
                automato.estado_6,
                "[\']",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
           automato.estado_1.gerarTransicao(
               automato.estado_7,
               "[\"]",
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

        automato.adicionaTransicao(
            automato.estado_6.gerarTransicao(
                automato.estado_6,
                "[^\']",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_6.gerarTransicao(
                automato.estado_1,
                "'",
                self.criarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_7.gerarTransicao(
                automato.estado_7,
                "[^\"]",
                self.incrementarToken
            )
        )

        automato.adicionaTransicao(
            automato.estado_7.gerarTransicao(
                automato.estado_1,
                "[\"]",
                self.criarToken
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
        self.contLinha        = 1
        self.contColuna       = 1

        for linha in self.linhasArquivoCompilar:
            linha = linha.replace(chr(9), '')
            linha = linha.replace(chr(10), '')
            self.contColuna       = 1
            for caracter in linha:
                self.charLidoAtual = caracter
                self.lerCaracter(caracter)

                self.contColuna += self.contColuna

            self.contLinha += 1

        if self.stringTokenAtual != '':
            self.finalizarToken()


    def incrementarToken(self):
        self.stringTokenAtual += self.charLidoAtual


    def finalizarToken(self):
        if self.stringTokenAtual in self.listaCaracteresEspeciais:
            tipoToken = 'caracterEspecial'
        elif self.stringTokenAtual in self.listaPalavrasChave:
            tipoToken = 'palavrachave'
        elif self.stringTokenAtual.isnumeric():
            tipoToken = 'constante'
        else:
            tipoToken = 'identificador'

        self.listaTokens.append(Token(self.stringTokenAtual, tipoToken, self.contLinha))
        self.stringTokenAtual = ''


    def criarToken(self):
        self.incrementarToken()
        self.finalizarToken()


    def finalizarTokenCriarToken(self):
        self.finalizarToken()
        self.criarToken()


    def erroLexico(self):
        raise Exception(
            "Caracter inexperado: " +  self.charLidoAtual +
            ". Linha: "  + str(self.contLinha) +
            ", Coluna: " + str(self.contColuna) + '.'
        )


if __name__ == "__main__":
    analisador = AnalisadorLexico()
    analisador.carregaListaCaracteresEspeciais("specialTokens.json")
    analisador.carregaListaPalavrasChave("keywords.json")
    analisador.carregaArquivoCompilar("samples/Jogo de Boca.cpp")
    #analisador.carregaArquivoCompilar("samples/input.txt")
    #analisador.carregaArquivoCompilar("samples/program.c")
    #analisador.carregaArquivoCompilar("samples/Cliente.java")
    #analisador.carregaArquivoCompilar("samples/simple.cpp")
    #analisador.carregaArquivoCompilar("samples/simple.txt")
    analisador.constroiAutomato()
    analisador.parsearTokens()
    print(analisador.listaTokens)