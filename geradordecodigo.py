import analisadorlexico
class GeradorDeCodigo:

    def __init__(self):
        self.fluxoTokens = list()
        self.listaIdentificadores = list()
        self.contLabel = 1
        self.tradutorAcoes = {
            'main' : self.main_function,
            'int': self.int_function,
            'scanf': self.leit_function,
            'atribuicao': self.atribuicao_funtion,
            'printf': self.print_function,
            'if': self.cond_function,
            'while' : self.loop_function,
        }


    def carregar_codigo_fonte(self, caminho):
        analisador = analisadorlexico.AnalisadorLexico()
        analisador.carregaListaCaracteresEspeciais(r"C:\Users\user\Desktop\5 Semestre\Compiladores\Trabalhos\Compilador\specialTokens.json")
        analisador.carregaListaPalavrasChave(r"C:\Users\user\Desktop\5 Semestre\Compiladores\Trabalhos\Compilador\keywords.json")
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
            # listaRetorno.append('ARMZ ' + str(self.listaIdentificadores.index(str(token))))
            listaRetorno.append('ARMZ ' + str(token))
        except ValueError:
            raise Exception('Identificador ' + str(token) + ' inexistente')

        return listaRetorno


    def atribuicao_funtion(self, token):
        while self.fluxoTokens.pop(0) != '=':
            pass

        instrucoes = self.expressao_function()
        instrucoes.append('ARMZ ' + str(token))
        # instrucoes.append('ARMZ ' + str(self.listaIdentificadores.index(str(token))))
        return instrucoes



    def expressao_function(self):
        instrucoes = list()

        while True:
            token = self.fluxoTokens.pop(0)

            if token.tipo == 'constante':
                instrucoes.append('CRCT ' + str(token))

            elif token.tipo == 'identificador':
                # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(token))))
                instrucoes.append('CRVL ' + str(token))

            elif str(token) == '+':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append('SOMA')

            elif str(token) == '-':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append('SUBT')

            elif str(token) == '/':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append('DIVI')

            elif str(token) == '*':
                proximoToken = self.fluxoTokens.pop(0)

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' +str(proximoToken))

                instrucoes.append('MULT')

            elif str(token) == '>':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CMMA'
                # Se for >= , remove mais um token
                if proximoToken == '=':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'CMAG'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

            elif str(token) == '<':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CMME'
                # Se for <= , remove mais um token
                if proximoToken == '=':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'CMEG'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

            elif str(token) == '=':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CCC'
                # Se for == , remove mais um token
                if proximoToken == '=':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'CMIG'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

            elif str(token) == '!':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CCC'
                # Se for == , remove mais um token
                if proximoToken == '=':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'CMDG'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

            elif str(token) == '&':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CCC'
                # Se for == , remove mais um token
                if proximoToken == '&':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'CONJ'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

            elif str(token) == '|':
                proximoToken = self.fluxoTokens.pop(0)

                codInstrucao = 'CCC'
                # Se for == , remove mais um token
                if proximoToken == '|':
                    proximoToken = self.fluxoTokens.pop(0)
                    codInstrucao = 'DISJ'

                # Verifica se o proixmo token é constante ou identificador
                if proximoToken.tipo == 'constante':
                    instrucoes.append('CRCT ' + str(proximoToken))

                elif proximoToken.tipo == 'identificador':
                    # instrucoes.append('CRVL ' + str(self.listaIdentificadores.index(str(proximoToken))))
                    instrucoes.append('CRVL ' + str(proximoToken))

                instrucoes.append(codInstrucao)

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


    def cond_function(self):
        # Recupera a primeira etapa do if que é a condicao
        while self.fluxoTokens.pop(0) != '(':
            pass

        listaInstrucoes = list()
        # Realiza a leitura da expressao
        listaInstrucoes += self.expressao_function()
        # Armazena uma label para o salto caso a intrucao seja false
        labelIF = self.get_next_label()
        # Apos a expressao armazena o pulo para a label
        listaInstrucoes.append("DSVF " + labelIF)

        # Verifica se proximo caracter é }
        if self.fluxoTokens[0] == '{':
            # Remove o caracter '{'
            self.fluxoTokens.pop(0)

            #  Aguarda o caracter '}'
            while self.fluxoTokens[0] != '}':
                # processa a intrucao dentro do if
                listaInstrucoes += self.processa_instrucao()

            # Remove o caracter '}'
            self.fluxoTokens.pop(0)

        else :
            # processa somente uma instrucao
            listaInstrucoes += self.processa_instrucao()


        # verifica se a proxima instrucao é um else
        if str(self.fluxoTokens[0]) == 'else':

            # Cria uma label para o else
            labelENDIF = self.get_next_label()

            # Adiciona a instrucao para pular o if pular o else
            listaInstrucoes.append("DSVS " + labelENDIF)

            # Apos o processamento da instrucao adiciona o label do pulo
            listaInstrucoes.append(labelIF)

            # Remove o else
            self.fluxoTokens.pop(0)

            # Verifica se proximo caracter é }
            if self.fluxoTokens[0] == '{':
                # Remove o caracter '{'
                self.fluxoTokens.pop(0)

                #  Aguarda o caracter '}'
                while self.fluxoTokens[0] != '}':
                    # processa a intrucao dentro do if
                    listaInstrucoes += self.processa_instrucao()

                # Remove o caracter '}'
                self.fluxoTokens.pop(0)

            else :
                # processa somente uma instrucao
                listaInstrucoes += self.processa_instrucao()

            # infaliza o else
            listaInstrucoes.append(labelENDIF)
        else :
            # Adiciona a label do endif
            listaInstrucoes.append(labelIF)

        return listaInstrucoes


    def loop_function(self):
        labelWhile = self.get_next_label()
        listaInstrucoes = [labelWhile]

        # Recupera a primeira etapa do while que é a condicao
        while self.fluxoTokens.pop(0) != '(':
            pass

        # Realiza a leitura da expressao
        listaInstrucoes += self.expressao_function()

        # Recupera uma label para o endwhile
        labelEndWhile = self.get_next_label()

        # insere a label da expressao do fim do while
        listaInstrucoes.append('DSVF ' + labelEndWhile)

        # Verifica se proximo caracter é }
        if self.fluxoTokens[0] == '{':
            # Remove o caracter '{'
            self.fluxoTokens.pop(0)

            #  Aguarda o caracter '}'
            while self.fluxoTokens[0] != '}':
                # processa a intrucao dentro do if
                listaInstrucoes += self.processa_instrucao()

            # Remove o caracter '}'
            self.fluxoTokens.pop(0)

        else :
            # processa somente uma instrucao
            listaInstrucoes += self.processa_instrucao()

        listaInstrucoes.append('DSVS ' + labelWhile)
        listaInstrucoes.append(labelEndWhile)

        return listaInstrucoes


    def get_next_label(self):
        label = 'L' + str(self.contLabel)
        self.contLabel += 1
        return label


    def traduzir(self):
        self.listaInstrucoes = list()
        # Percorre cada token do fluxo
        while len(self.fluxoTokens) > 0:
            self.listaInstrucoes += self.processa_instrucao()


    def processa_instrucao(self):
        listaInstrucoes = list()
            # Recupera o token atual
        try:
            token = self.fluxoTokens.pop(0)

            # Executa o procedimento de tratamento do token
            listaInstrucoes += self.tradutorAcoes[str(token)]()
        except KeyError:
            if token.tipo == 'identificador':
                listaInstrucoes += self.tradutorAcoes['atribuicao'](token)

        return listaInstrucoes


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
    gerador.carregar_codigo_fonte(r'C:\Users\user\Desktop\5 Semestre\Compiladores\Trabalhos\Compilador\samples\input_gerador.cpp')
    # print(gerador.fluxoTokens)
    gerador.traduzir()
    gerador.printa_resultado()

