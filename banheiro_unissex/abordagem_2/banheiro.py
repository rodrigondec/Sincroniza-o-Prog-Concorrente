import time
from random import randrange
from threading import Thread, Lock, Condition


# VARIÁVEIS DE CONFIGURAÇÃO
limite_pessoas = 7


class Banheiro(object):
    """Implementação de um banheiro"""
# TODO documentar variáveis

    def __init__(self, limite_pessoas, limite_pessoas_por_genero):
        """Constructor for Banheiro"""
        # variaaves
        self.limite_pessoas = limite_pessoas #max de pessoas ao mesmo tempo

        #qtd maxima de pessoas de um gênero que podem usar o banheiro antes
        #de trocar o gênero
        self.limite_pessoas_por_genero = limite_pessoas_por_genero

        self.pessoas = 0
        self.genero_atual = "" #possible values: "" "M" or "F"
        self.pessoas_usando = [] #pessoas usando o banheiro no momento
        self.fila = []
        self.finish = False
        
        #locks
        self.fila_lk = Lock() #apenas um lock é criado para alterar os dados da fila
        self.banheiro_lk = Lock() #lock para lista de pessoas que estão usando o banheiro
        #idealmente 2 poderiam ser criados, caso a fila fosse encadeada

        #variáveis condicionais
        self.fila_cv = Condition(self.fila_lk)
        self.banheiro_cv = Condition(self.banheiro_lk)

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.finish:
            self.fila_lk.acquire()
            self.banheiro_lk.acquire()

            if len(self.fila) == 0 and len(self.pessoas_usando) == 0:
                #fila e banheiros vazios. Esperar alguém entrar na fila
                self.banheiro_lk.release()
                self.fila_cv.wait()
                self.fila_lk.release()
                continue #continue pois pode ter sido chamado para terminar execução

            if len(self.pessoas_usando) == self.limite_pessoas:
                #banheiro está cheio. Esperar liberar 1 espaço
                self.fila_lk.release() #permite que novas pessoas entrem na fila

                #pode travar locks fora de ordem pois quem está na fila não irá
                #executar nenhuma ação sem antes ser acordado por este método
                self.banheiro_cv.wait()
                self.banheiro_lk.release()
                continue

            if len(self.fila) != 0:
                #alguém na fila pode entrar no banheiro.
                self.fila[0].cv.notify()
                #esperar ação de dentro do banheiro (ou entrada ou saída)
            
            #else: fila está vazia. Não se sabe se chegarão mais funcionários.
            #Esperar um dos que estão no banheiro sair.
            self.fila_lk.release()
            self.banheiro_cv.wait()
            self.banheiro_lk.release()

    def end_loop(self):
        self.finish = True
        self.fila_lk.acquire()
        self.fila_cv.notify()
        self.fila_lk.release()


class Pessoa(object):
    """Implementação de um banheiro"""
    id_pessoa = 1
    def __init__(self, sexo, banheiro):
        """Constructor for Pessoa"""
        self.id_pessoa = Pessoa.id_pessoa
        Pessoa.id_pessoa += 1
        self.sexo = sexo
        self.banheiro = banheiro
        self.thread = Thread(target=self.run)
        self.cv = Condition(self.banheiro.fila_lk)

        self.thread.start()

    def run(self):
        self.trabalhar()
        self.entrar_fila()
        self.entrar_banheiro()
        self.usar_banheiro()
        self.sair()

    def trabalhar(self):
        tempo = randrange(60) #cada segundo simula 1 minuto de uma hora
        print("TRABALHA POR " + str(tempo) + " SEGUNDOS: " + str(self))
        time.sleep(tempo)

    def entrar_fila(self):
        self.banheiro.fila_lk.acquire()
        print("ENTRA FILA " + str(self))
        #se adiciona na fila
        self.banheiro.fila.append(self)
        #notifica à fila que uma nova pessoa entrou nela
        self.banheiro.fila_cv.notify()
        self.banheiro.banheiro_lk.acquire() #evita idle management quando,
        self.banheiro.banheiro_cv.notify() #por exemplo, fila está vazia e
        self.banheiro.banheiro_lk.release() #está esperando alguém sair do banheiro

        #espera ser acordado. Quando é acordado entra no banheiro
        self.cv.wait()
        self.banheiro.banheiro_lk.acquire()


    def entrar_banheiro(self):
        self.banheiro.fila.remove(self)
        self.banheiro.fila_lk.release()
        self.banheiro.pessoas_usando.append(self)
        print("ENTRA BANHEIRO " + str(self) + "\tqtd_pessoas_no_banheiro: " +
            str(len(self.banheiro.pessoas_usando)))
        self.banheiro.banheiro_cv.notify() #acorda banheiro
        self.banheiro.banheiro_lk.release()

    def usar_banheiro(self):
        tempo = randrange(4) + 1 #cada segundo simula 1 minuto de uma hora
        print("USA BANHEIRO POR " + str(tempo) + " SEGUNDOS " + str(self))
        time.sleep(tempo)
        

    def sair(self):
        self.banheiro.banheiro_lk.acquire()
        self.banheiro.pessoas_usando.remove(self)
        print("SAIR " + str(self) + "\t\tqtd_pessoas_no_banheiro: " + 
            str(len(self.banheiro.pessoas_usando)))
        self.banheiro.banheiro_cv.notify() #acorda banheiro para que ele possa colocar
        #mais gente pra dentro
        self.banheiro.banheiro_lk.release()

    def __str__(self):
        return str(self.id_pessoa) + " " + self.sexo

banheiro = Banheiro(limite_pessoas, 0)

pessoas = []

for x in range(60):
    pessoas.append(Pessoa('M', banheiro))
    pessoas.append(Pessoa('F', banheiro))

for x in range(len(pessoas)):
    pessoas[x].thread.join()

banheiro.end_loop()