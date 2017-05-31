import os
import sys
import time
from random import randrange
from threading import Thread, Condition, Barrier, Lock, Semaphore
from logging import getLogger, Formatter, FileHandler, StreamHandler, INFO


def setup_logger(logger_name, log_file, level=INFO):
    l = getLogger(logger_name)
    formatter = Formatter('%(message)s')
    fileHandler = FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

setup_logger("info_log", "info.log")
info_log = getLogger("info_log")

setup_logger("carro_log", "carro.log")
carro_log = getLogger("carro_log")

setup_logger("passageiros_log", "passageiros.log")
passageiros_log = getLogger("passageiros_log")

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


# global variables
curr_car = None
fila_cv = None
fila = []

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
        self.passageiros = [] #passageiros dentro do carro

        self.barr = Barrier(limite_pessoas + 1)  # usado para esperar por saida (passageiros + carro)
        self.lk = Lock()  # usado para garantir corretude (travar a lista de passageiros)
        self.sem = Semaphore()  # semaphore is going to be used for controlling unboarding

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
        
        for i in range(self.limite_pessoas):
            global fila
            global fila_cv
            fila_cv.acquire()
            #acorda a quantidade de pessoas necessárias para fazer o carro andar
            if len(fila) == 0: #fila vazia. Esperar alguém entrar
                fila_cv.wait()
            #remove um cara da fila e o notifica para entrar no carro
            passageiro = fila.pop(0)
            fila_cv.release()
            passageiro.cv.acquire()
            passageiro.cv.notify()
            passageiro.cv.release()
        

        #esperar pessoas acordadas embarcarem / carro ficar cheio
        self.lk.acquire()
        #if necessário pois é possível que todos os passageiros entrem no carro antes de wait() ser chamado. Causando
        #livelock. Carro e passageiros irão dormir eternamente
        if len(self.passageiros) < self.limite_pessoas:
            self.cv_car.wait()

        global curr_car
        curr_car = self.prv_car  # this is done so passengers try to enter the new car
        self.prv_car.sem.release()  # wakes up previous car

    def unload(self, last_trip):
        self.sem.acquire()  # use for cars' arrival order
        print_carro_log("Carro: " + str(self) + " passeio terminado!")
        # it is done before barr.wait so the car thread can sleep before any passenger leaves
        self.barr.wait()  # releases passengers
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.cv_car.wait()  # wait until it is empty
        print_carro_log("Carro: " + str(self) + " desembarque do carro está vazio!")
        self.lk.release()

        self.prv_car.sem.release()  # permite o carro anterior liberar passageiros

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
        self.cv = Condition()
        Passageiro.id_passageiro += 1

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            self.entrar_fila()
            self.board()
            self.unboard()
            self.passear()

    def entrar_fila(self):
        global fila
        global fila_cv
        fila_cv.acquire()
        fila.append(self) #se adiciona na fila. Valor de curr_car não importa
        print_passageiros_log("Passageiro: " + str(self) + " entrou na fila " + " ".join(str(x) for x in fila))
        fila_cv.notify() #acorda carro para indicar que entrou uma pessoa na fila
        self.cv.acquire()
        fila_cv.release()
        self.cv.wait() #espera ser o primeiro da fila para entrar
        self.cv.release()

    def passear(self):
        tempo = randrange(5) + 1
        print_passageiros_log("Passageiro: " + str(self) + " vai passear no parque por " + str(
            tempo) + " segundos enquanto Seu Lobo não vem.")
        time.sleep(tempo)

    def board(self):
        #se chega nesse ponto, foi acordado. (primeiro da fila)
        global curr_car
        self.carro_atual = curr_car  # curr_car is a global variable
        print_passageiros_log("Passageiro: " + str(self) + " vai tentar entrar no carro " + str(self.carro_atual))
        self.carro_atual.lk.acquire()
        self.carro_atual.passageiros.append(self)
        # mensagem impressa dentro de lock para facilitar compreensao. Idealmente estaria fora
        print_passageiros_log(
            "Passageiro: " + str(self.id_passageiro) + " entrou no carro " + str(self.carro_atual) + "! " +
            str(len(self.carro_atual.passageiros)))
        if len(self.carro_atual.passageiros) == self.carro_atual.limite_pessoas:
            self.carro_atual.cv_car.notify()  # Car is full and will start running

        self.carro_atual.lk.release()
        self.carro_atual.barr.wait()

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

carros = []
fila_cv = Condition()

# inicializa carros
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

for x in range(num_pessoas):
    p = Passageiro()
    #passageiros.append(p)

carros[qtd_carros - 1].thread_main.join()
os._exit(1)
