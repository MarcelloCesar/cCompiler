import analisadorlexico
class GeradorDeCodigo:

    def __init__(self):
        self.fluxoTokens = list()
        self.listaIdentificadores = list()
        self.tradutorAcoes = {
            'main' : self.main_function,
            'int': self.int_function,
            'scanf': self.leit_function,
            'atribuicao': self.atribuicao_funtion,
            'printf': self.print_function
        }


    def carregar_codigo_fonte(self, caminho):
        analisador = analisadorlexico.AnalisadorLexico()
        analisador.carregaListaCaracteresEspeciais("specialTokens.json")
        analisador.carregaListaPalavrasChave("keywords.json")
        analisador.carregaArquivoCompilar(caminho)
        analisador.constroiAutomato()
        analisador.parsearTokens()
        self.fluxoTokens = analisador.listaTokens


    def main_function(self):
        # Retorna a instrucao de inicio de programa principal
        return ['INPP']


    def int_function(self):
        # Inicializa o contador que determina quantas posicoes de memoria alocar
        contadorMemoria = 0

        # Continua buscando o fluxo de tokens ate encontrar uma virgula ou ponto e virgula
        # a virgula significa que existe um novo token
        while True:
            # recupera o proximo token
            token = self.fluxoTokens.pop(0)

            # se encontrou ponto e virgula quebra o loop
            if str(token) == ';':
                break

            # se o token não for uma virgula adiciona um contador
            if str(token) != ',':
                contadorMemoria += 1

                if token.tipo == 'identificador':
                    self.listaIdentificadores.append(str(token))

        return ['AMEM ' +  str(contadorMemoria)]


    def leit_function(self):
        # Faz a leitura dos tokens até encontrar o token &
        while self.fluxoTokens.pop(0) != '&':
            pass

        # Realiza a leitura do identificador após o caracter &
        token = self.fluxoTokens.pop(0)

        # Termina a leitura da instrucao
        while self.fluxoTokens.pop(0) != ';':
            pass

        listaRetorno = list()
        listaRetorno.append('LEIT')
        try:
            listaRetorno.append('ARMZ ' + str(self.listaIdentificadores.index(str(token))))
        except ValueError:
            raise Exception('Identificador ' + str(token) + ' inexistente')

        return listaRetorno


    def atribuicao_funtion(self, token):
        while self.fluxoTokens.pop(0) != '=':
            pass

        instrucoes = self.expressao_function()
        instrucoes.append('ARMZ ' + str(self.listaIdentificadores.index(str(token))))
        return instrucoes



    def expressao_function(self):
        instrucoes = list()

        while True:
            token = self.fluxoTokens.pop(0)

            if token.tipo == 'constante':
                instrucoes.append('CRCT ' + str(token))

            elif token.tipo == 'identificador':
                instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(token))))

            elif str(token) == '+':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))

                instrucoes.append('SOMA')

            elif str(token) == '-':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))

                instrucoes.append('SUBT')

            elif str(token) == '/':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))

                instrucoes.append('DIVI')

            elif str(token) == '*':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))

                instrucoes.append('MULT')

            elif str(token) in [',', ';', ')']:
                break

        return instrucoes


    def print_function(self):
        while self.fluxoTokens.pop(0) != ',':
            pass

        instrucoes = list()

        while True:
            instrucoes += self.expressao_function()
            instrucoes.append('IMPR')

            # Verifica se eh o ponto e virgula apos parentesis de fechamendo do printf
            if self.fluxoTokens[0] == ';':
                # Remove o ponto e virgula
                self.fluxoTokens.pop(0)

                # encerra o printf
                break

        return instrucoes

    def traduzir(self):
        self.listaInstrucoes = list()
        # Percorre cada token do fluxo
        while len(self.fluxoTokens) > 0:
            try:
                # Recupera o token atual
                token = self.fluxoTokens.pop(0)

                # Executa o procedimento de tratamento do token
                self.listaInstrucoes += self.tradutorAcoes[str(token)]()
            except KeyError:
                if token.tipo == 'identificador':
                    self.listaInstrucoes += self.tradutorAcoes['atribuicao'](token)


    def printa_resultado(self):
        # Adiciona as constantes de finalizacao
        self.listaInstrucoes.append(
            'DMEM ' + str(len(self.listaIdentificadores))
        )

        self.listaInstrucoes.append(
            'PARA'
        )

        for i in self.listaInstrucoes:
            print(i)



if __name__ == '__main__':
    gerador = GeradorDeCodigo()
    gerador.carregar_codigo_fonte('samples/input_gerador.cpp')
    # print(gerador.fluxoTokens)
    gerador.traduzir()
    gerador.printa_resultado()

