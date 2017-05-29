import logging
import time
import os
from random import randrange
from threading import Thread, Condition, Barrier, Lock, Semaphore
import sys

# global variables
curr_car = None


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)


setup_logger("info_log", "info.log")
info_log = logging.getLogger("info_log")

setup_logger("carro_log", "carro.log")
carro_log = logging.getLogger("carro_log")

setup_logger("passageiros_log", "passageiros.log")
passageiros_log = logging.getLogger("passageiros_log")


def print_info_log(msg):
    info_log.info(msg)


def print_carro_log(msg):
    print(msg)
    carro_log.info(msg)
    print_info_log(msg)


def print_passageiros_log(msg):
    print(msg)
    passageiros_log.info(msg)
    print_info_log(msg)


class Erro(Exception):
    def __init__(self, msg):
        self.msg = msg


"""
Essa abordagem irá fazer o uso de barreiras. É impossível o uso de barreiras para controlar a entrada e saída.
As barreiras são utilizadas para controlar apensas a saída dos passageiros dos veículos, pois um número fixo de
threads é necessário para reativar a barreira. Isso não pode ser feito para a entrada no carro. Considere o caso
em que o caro possui 5 vagas mas há 11 pessoas no parque, das quais 5 estão no veículo, 4 na fila e 2 passeando.
A "barreira" de entrada ficará bloqueada até que 6 threads a desbloqueiem (1 pro carro e 5 para os passageiros).
Entretanto, quando as 2 pessoas que estiverem passeando entrarem na fila, tentarão entrar no veículo que pode não
ter sido unloaded ainda. Por esse motivo, CVs foram usadas para controlar a entrada.
"""


class Carro(object):
    """Carro de uma montanha russa"""
    id = 1

    def __init__(self, limite_pessoas, num_passeios):  # ,
        # barreira, lock, condition_variable): #barreira, lock e condition_variables necessitam ser os mesmos enviados
        # aos passageiros
        """Constructor for Car"""
        self.id = Carro.id
        Carro.id += 1

        self.limite_pessoas = limite_pessoas
        self.num_passeios = num_passeios
        self.passageiros = []

        self.barr = Barrier(limite_pessoas + 1)  # usado para esperar por saida (passageiros + carro)
        self.lk = Lock()  # usado para garantir corretude (travar a lista de passageiros)
        self.sem = Semaphore()  # semaphore is going to be used for controlling unboarding

        # e para cvs (controlar board e unboard)
        self.boardable = False
        self.cv_list = Condition(lock=self.lk)  # usado para esperar carro ficar vazio
        self.cv_car = Condition(lock=self.lk)  # usado para controle do algoritmo main do carro

        self.prv_car = None  # usado para acordar carro anterior, permitindo que novos passageros embarquem nele

        self.thread_main = None

    def set_prv_car(self, prv_car):
        self.prv_car = prv_car

    def set_thread_main_args(self, is_car_sleeping):
        self.thread_main = Thread(target=self.main, args=(is_car_sleeping,))

    # def main(self, is_sleeping):
    def main(self, is_sleeping):
        if (is_sleeping):  # waits for next car to get full and free this
            self.sem.acquire()

        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " passeio nº " + str(x + 1))

            print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
            self.load()

            print_carro_log("Carro: " + str(self) + " espera terminar o passaio para liberar desembarque!")
            self.run()

            print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar embarque!")
            if x != self.num_passeios - 1:
                self.unload(False)
            else:
                self.unload(True)

        print("\t\nACABEI\n")

    def run(self):
        print_carro_log("Carro: " + str(self) + " passeio iniciado!")
        tempo = 5  # passeia por 5 segundos. Tempo constatne para simular questao de seguranca na montanha
        print_carro_log("Carro: " + str(self) + " vai andar por " + str(tempo) + " segundos.")
        time.sleep(tempo)

    def load(self):
        print_carro_log("Carro: " + str(self) + " embarque do carro está liberado!")
        self.lk.acquire()  # usado para corretude
        self.cv_list.notify_all()  # wakes up all sleeping passengers threads that tried to enter this car before
        # it has become available to boarding
        self.boardable = True  # this will allow the passengers to board
        self.cv_car.wait()  # espera carro ficar cheio
        global curr_car
        curr_car = self.prv_car  # this is done to avoid passengers trying to enter curr_car (self) twice
        self.cv_list.notify_all()  # wakes up all sleeping passengers threads (passengers that tried to enter
        # after car getting full. This is necessary so they can attempt to enter the next car)
        self.prv_car.sem.release()  # wakes up previous car
        self.lk.release()  # usado para corretude

    def unload(self, last_trip):
        self.lk.acquire()  # lock needs to be acquired before cv_wait to assure corretude. Used for passengers
        self.sem.acquire()  # use for cars' arrival order
        print_carro_log("Carro: " + str(self) + " passeio terminado!")
        # it is done before barr.wait so the car thread can sleep before any passenger leaves
        self.barr.wait()  # releases passengers
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.cv_car.wait()  # wait until it is empty
        print_carro_log("Carro: " + str(self) + " desembarque do carro está vazio!")

        self.prv_car.sem.release()  # permite o carro anterior liberar passageiros

        self.lk.release()  # (once it is notified, it will "reacquire" lock)
        if not last_trip:
            self.sem.acquire()  # waits next car to get full

    def __str__(self):
        return str(self.id)


class Passageiro(object):
    """Passageiros de uma montanha russa"""

    id_passageiro = 1

    def __init__(self):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        self.carro_atual = None  # carro no qual o passageiro entrou ou vai tentar entrar
        Passageiro.id_passageiro += 1

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            self.board()
            self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5) + 1
        print_passageiros_log("Passageiro: " + str(self) + " vai passear no parque por " + str(
            tempo) + " segundos enquanto Seu Lobo não vem.")
        time.sleep(tempo)

    def board(self):
        global curr_car
        while (True):
            self.carro_atual = curr_car  # curr_car is a global variable
            print_passageiros_log("Passageiro: " + str(self) + " vai tentar entrar no carro " + str(self.carro_atual))
            self.carro_atual.lk.acquire()
            if not self.carro_atual.boardable:
                self.carro_atual.cv_list.wait()
                self.carro_atual.lk.release()
                continue

            self.carro_atual.passageiros.append(self)
            # mensagem impressa dentro de lock para facilitar compreensao. Idealmente estaria fora
            print_passageiros_log(
                "Passageiro: " + str(self.id_passageiro) + " entrou no carro " + str(self.carro_atual) + "! " +
                str(len(self.carro_atual.passageiros)))
            if len(self.carro_atual.passageiros) == self.carro_atual.limite_pessoas:
                self.carro_atual.cv_car.notify()  # Car is full and will start running
                self.carro_atual.boardable = False  # Done here to ensure corretude.
            barr = self.carro_atual.barr  # salvo em variavel local para garantir coretude (caso fosse salvo depois do lock ser solto, valor de)
            self.carro_atual.lk.release()
            barr.wait()
            break

    def unboard(self):
        print_passageiros_log("Passageiro: " + str(self) + " vai tentar sair do carro " + str(self.carro_atual))
        self.carro_atual.lk.acquire()
        self.carro_atual.passageiros.remove(self)
        if len(self.carro_atual.passageiros) == 0:
            self.carro_atual.cv_car.notify()
        # mensagem impressa dentro de lock para facilitar compreensao. Idealmente estaria fora
        print_passageiros_log("Passageiro: " + str(self.id_passageiro) + " saiu do carro!")
        self.carro_atual.lk.release()
        self.carro_atual = None

    def __str__(self):
        return str(self.id_passageiro)


# VARIÁVEIS DE CONFIGURAÇÃO

if len(sys.argv) != 5:
    print("Número inválido de argumentos. Exatamente 3 argumentos requeridos, na seguinte ordem:" +
          "\n1 - Número total de passageiros\n2 - Capacidade do carro\n3 - Número máximo de passeios" +
          "\n4 - Quantidade de carros")
    os._exit(1)

num_pessoas = None
limite_pessoas_por_carro = None
passeios_por_carro = None
qtd_carros = None

try:
    num_pessoas = int(sys.argv[1])
    limite_pessoas_por_carro = int(sys.argv[2])
    passeios_por_carro = int(sys.argv[3])
    qtd_carros = int(sys.argv[4])
except ValueError:
    print("Argumento(s) inválido(s)! Os 4 argumentos enviados necessitam ser do tipo inteiro")
    os._exit(1)

if (num_pessoas < limite_pessoas_por_carro):
    print("Erro! Número total de pessoas/passageiros é menor que a capacidade do carro")
    os._exit(1)

# inicializa carros
carros = []
carros.append(Carro(limite_pessoas_por_carro, passeios_por_carro))  # sets first car
carros[0].set_thread_main_args(False)
for i in range(qtd_carros - 1):
    carros.append(Carro(limite_pessoas_por_carro, passeios_por_carro))
    carros[i + 1].set_thread_main_args(True)
    carros[i].set_prv_car(carros[i + 1])
    carros[i + 1].sem.acquire()  # bloqueia carro na chegada, garantindo ordem
# finishes setting first car
carros[qtd_carros - 1].set_prv_car(carros[0])

# defines first current car (car to be boarded)
curr_car = carros[0]  # global

# Starts all threads
for i in range(qtd_carros):
    carros[i].thread_main.start()

passageiros = []
for x in range(num_pessoas):
    passageiros.append(Passageiro())

carros[qtd_carros - 1].thread_main.join()
os._exit(1)
