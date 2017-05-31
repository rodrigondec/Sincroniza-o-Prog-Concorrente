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
        self.limite_pessoas = limite_pessoas  # max de pessoas ao mesmo tempo

        # qtd maxima de pessoas de um gênero que podem usar o banheiro antes
        # de trocar o gênero
        self.limite_pessoas_por_genero = limite_pessoas_por_genero

        self.pessoas = 0
        self.genero_atual = ""  # possible values: "" "M" or "F"
        self.pessoas_usando = []  # pessoas usando o banheiro no momento
        self.fila = []
        self.finish = False

        # locks
        self.fila_lk = Lock()  # apenas um lock é criado para alterar os dados da fila
        self.banheiro_lk = Lock()  # lock para lista de pessoas que estão usando o banheiro
        # idealmente 2 poderiam ser criados, caso a fila fosse encadeada

        # variáveis condicionais
        self.fila_cv = Condition(self.fila_lk)
        self.banheiro_cv = Condition(self.banheiro_lk)

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.finish:
            self.fila_lk.acquire()
            self.banheiro_lk.acquire()

            if len(self.fila) == 0 and len(self.pessoas_usando) == 0:
                # fila e banheiros vazios. Esperar alguém entrar na fila
                self.banheiro_lk.release()
                self.fila_cv.wait()
                self.fila_lk.release()
                continue  # continue pois pode ter sido chamado para terminar execução

            if len(self.pessoas_usando) == self.limite_pessoas:
                # banheiro está cheio. Esperar liberar 1 espaço
                self.fila_lk.release()  # permite que novas pessoas entrem na fila

                # pode travar locks fora de ordem pois quem está na fila não irá
                # executar nenhuma ação sem antes ser acordado por este método
                self.banheiro_cv.wait()
                self.banheiro_lk.release()
                continue

            if len(self.fila) != 0:
                # alguém na fila pode entrar no banheiro.
                self.notificar_proximo()
                # self.fila[0].cv.notify()
                # esperar ação de dentro do banheiro (ou entrada ou saída)

            # else: fila está vazia. Não se sabe se chegarão mais funcionários.
            # Esperar um dos que estão no banheiro sair.
            self.fila_lk.release()
            self.banheiro_cv.wait()
            self.banheiro_lk.release()

    def end_loop(self):
        self.finish = True
        self.fila_lk.acquire()
        self.fila_cv.notify()
        self.fila_lk.release()

    def notificar_proximo(self):
        if self.genero_atual == "":
            self.genero_atual = self.fila[0].sexo

        if self.fila[0].sexo == self.genero_atual:
            # notifica a cabeça
            self.fila[0].cv.notify()
            # incrementa o contador
            self.pessoas = min(self.pessoas + 1, self.limite_pessoas_por_genero)

        elif (self.fila[0].sexo != self.genero_atual and
                      self.pessoas < self.limite_pessoas_por_genero):
            # notificar a próxima pessoa do sexo oposto na fila, se existir.
            # só notifica se limite_pessoas_por_genero não foi atingido
            next_index = self.find_next(self.genero_atual, 1)
            if next_index > 0:
                self.fila[next_index].cv.notify()
                self.pessoas += 1

    def find_next(self, genero, start_index):
        for i in range(start_index, len(self.fila)):
            if self.fila[i].sexo == genero:
                return i
        return -1

    def trocar_genero(self):
        if len(self.pessoas_usando) == 0:
            self.genero_atual = ""
            self.pessoas = 0
            # print("\tGENERO: " + self.genero_atual)


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
        tempo = randrange(60)  # cada segundo simula 1 minuto de uma hora
        print("TRABALHA POR " + str(tempo) + " SEGUNDOS: " + str(self))
        time.sleep(tempo)

    def entrar_fila(self):
        self.banheiro.fila_lk.acquire()
        # print("ENTRA FILA " + str(self))
        # se adiciona na fila
        self.banheiro.fila.append(self)
        print("ENTRA FILA: " + " ".join(str(s) for s in self.banheiro.fila))
        # notifica à fila que uma nova pessoa entrou nela
        self.banheiro.fila_cv.notify()
        self.banheiro.banheiro_lk.acquire()  # evita idle management quando,
        self.banheiro.banheiro_cv.notify()  # por exemplo, fila está vazia e
        self.banheiro.banheiro_lk.release()  # está esperando alguém sair do banheiro

        # espera ser acordado. Quando é acordado entra no banheiro
        self.cv.wait()
        self.banheiro.banheiro_lk.acquire()

    def entrar_banheiro(self):
        self.banheiro.fila.remove(self)
        self.banheiro.fila_lk.release()
        self.banheiro.pessoas_usando.append(self)
        # print("ENTRA BANHEIRO " + str(self) + "\tqtd_pessoas_no_banheiro: " +
        #    str(len(self.banheiro.pessoas_usando)))
        print("ENTRA BANHEIRO: " + " ".join(str(x) for x in self.banheiro.pessoas_usando))
        self.banheiro.banheiro_cv.notify()  # acorda banheiro
        self.banheiro.banheiro_lk.release()

    def usar_banheiro(self):
        tempo = randrange(4) + 1  # cada segundo simula 1 minuto de uma hora
        # print("USA BANHEIRO POR " + str(tempo) + " SEGUNDOS " + str(self))
        time.sleep(tempo)

    def sair(self):
        self.banheiro.banheiro_lk.acquire()
        self.banheiro.pessoas_usando.remove(self)
        # print("SAIR " + str(self) + "\t\tqtd_pessoas_no_banheiro: " +
        #    str(len(self.banheiro.pessoas_usando)))
        print("SAIR BANHEIRO: " + " ".join(str(x) for x in self.banheiro.pessoas_usando))
        self.banheiro.trocar_genero()  # troca de genero quando necessario
        self.banheiro.banheiro_cv.notify()  # acorda banheiro para que ele possa colocar
        # mais gente pra dentro
        self.banheiro.banheiro_lk.release()

    def __str__(self):
        return str(self.id_pessoa) + "-" + self.sexo

# VARIÁVEIS DE CONFIGURAÇÃO
if len(sys.argv) != 4:
    print("Número inválido de argumentos. Exatamente 4 argumentos requeridos, na seguinte ordem:" +
          "\n1 - Número total de homens\n2 - Número total de mulheres\n3 - Número de vagas no banheiro")
    os._exit(1)

qt_homens = None
qt_mulheres = None
qt_vagas_banheiro = None

try:
    qt_homens = int(sys.argv[1])
    qt_mulheres = int(sys.argv[2])
    qt_vagas_banheiro = int(sys.argv[3])
except ValueError:
    print("Argumento(s) inválido(s)! Os 3 argumentos enviados necessitam ser do tipo inteiro")
    os._exit(1)

if qt_homens < qt_vagas_banheiro or qt_mulheres < qt_vagas_banheiro:
    print("Erro! Número total de homens ou mulheres é menor que a capacidade do banheiro")
    os._exit(1)

banheiro = Banheiro(qt_vagas_banheiro, 15)

pessoas = []
for x in range(qt_homens):
    pessoas.append(Pessoa('M', banheiro))

for x in range(qt_mulheres):
    pessoas.append(Pessoa('F', banheiro))

for x in range(len(pessoas)):
    pessoas[x].thread.join()

banheiro.end_loop()
