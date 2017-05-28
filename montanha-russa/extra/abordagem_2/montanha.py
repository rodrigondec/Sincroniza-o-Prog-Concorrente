import logging
import time
import os
from random import randrange
from threading import Thread, Condition, Barrier, Lock, Semaphore
import sys

#global variables
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

    def __init__(self, limite_pessoas, num_passeios, is_sleeping): #,
        #barreira, lock, condition_variable): #barreira, lock e condition_variables necessitam ser os mesmos enviados
        #aos passageiros
        """Constructor for Car"""
        self.id = id
        id += 1

        self.limite_pessoas = limite_pessoas
        self.num_passeios = num_passeios
        self.passageiros = []

        self.barr = Barrier(limite_pessoas + 1) #usado para esperar por saida (passageiros + carro)
        self.lk = Lock() #usado para garantir corretude (travar a lista de passageiros)
        self.sem = Semaphore() #semaphore is going to be used for controlling unboarding

        #e para cvs (controlar board e unboard)
        self.boardable = False
        self.cv_list = Condition(lock=self.lk) #usado para esperar carro ficar vazio
        self.cv_car = Condition(lock=self.lk) #usado para controle do algoritmo main do carro

        self.prv_car = None #usado para acordar carro anterior, permitindo que novos passageros embarquem nele

        self.thread_main = Thread(target=self.main, args=(is_sleeping))
        #self.thread_main.start()

    def set_prv_car(prv_car):
    	self.prv_car = prv_car

    def main(self, is_sleeping):
        if (is_sleeping): #waits for next car to get full and free this
        		self.lk.acquire()
        		self.cv_wait()
        		self.lk.release()

        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " passeio nº " + str(x + 1))

            print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
            self.load()

            print_carro_log("Carro: " + str(self) + " espera terminar o passaio para liberar desembarque!")
            self.run()

            print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar embarque!")
            self.unload()
        os._exit(1)

    def run(self):
        print_carro_log("Carro: " + str(self) + " passeio iniciado!")
        tempo = randrange(5) + 1
        print_carro_log("Carro: " + str(self) + " vai andar por " + str(tempo) + " segundos.")
        time.sleep(tempo)
        print_carro_log("Carro: " + str(self) + " passeio terminado!")

    def load(self):
        print_carro_log("Carro: " + str(self) + " embarque do carro está liberado!")
        self.lk.acquire() #usado para corretude
        self.cv_list.notify_all() #wakes up all sleeping passengers threads that tried to enter this car before
        #it has become available to boarding
        self.boardable = True #this will allow the passengers to board
        self.cv_car.wait() #espera carro ficar cheio
        #self.boardable = False #This is done at unboard to avoid adding more passengers than the max
        self.cv_list.notify_all() #wakes up all sleeping passengers threads (passengers that tried to enter
        #after car getting full. This is necessary so they can attempt to enter the next car)
        self.prv_car.lk.acquire() #no deadlock will happen since no one (passenger) will try to access this car
        #before the "curr_car = self.prv_car" instruction
        curr_car = self.prv_car #this is done to avoid passengers trying to enter curr_car (self) twice
        self.prv_car.lk.release()
        self.lk.release() #usado para corretude        

    def unload(self):
        self.lk.acquire() #lock needs to be acquired before cv_wait to assure corretude
        #it is done before barr.wait so the car thread can sleep before any passenger leaves
        self.barr.wait() #releases passengers
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.cv_car.wait() #wait until it is empty
        self.lk.release() #(once it is notified, it will "reacquire" lock)

    def __str__(self):
        return str(self.id)


class Passageiro(object):
    """Passageiros de uma montanha russa"""

    id_passageiro = 1

    def __init__(self):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        self.carro_atual = None #carro no qual o passageiro entrou ou vai tentar entrar
        Passageiro.id_passageiro += 1

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            self.board()
            self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_passageiros_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos enquanto Seu Lobo não vem.")
        time.sleep(tempo)

    def board(self):
        print_passageiros_log("Passageiro: " +str(self)+" vai tentar entrar no carro")
        while (True):
        	self.carro_atual = curr_car #curr_car is a global variable
	        self.carro_atual.lk.acquire()
	        if not self.carro_atual.boardable:
	        	self.carro_atual.cv_list.wait()
	        	self.carro_atual.lk.release()
	        	continue

	        self.carro_atual.passageiros.append(self)
	        #mensagem impressa dentro de lock para facilitar compreensao. Idealmente estaria fora
	        print_passageiros_log("Passageiro: " + str(passageiro.id_passageiro) + " entrou no carro!" + str(len(self.passageiros)))
	        if len(self.carro_atual.passageiros) == self.carro_atual.limite_pessoas:
	        	self.carro_atual.cv_car.notify() #Car is full and will start running
	        	self.carro_atual.boardable = False #Done here to ensure corretude.
	        barr = self.carro_atual.barr #salvo em variavel local para garantir coretude (caso fosse salvo depois do lock ser solto, valor de)
	        self.carro_atual.lk.release()
	        barr.wait()
	        break

    def unboard(self):
        print_passageiros_log("Passageiro: "+str(self)+" vai tentar sair do carro")
        self.carro_atual.lk.acquire()
        self.carro_atual.passageiros.remove(self)
        if len(self.carro_atual.passageiros) == 0:
        	self.carro_atual.cv_car.notify()
        #mensagem impressa dentro de lock para facilitar compreensao. Idealmente estaria fora
        print_passageiros_log("Passageiro: " + str(passageiro.id_passageiro) + " saiu do carro!")
        self.carro_atual.lk.release()
        self.carro_atual = None

    def __str__(self):
        return str(self.id_passageiro)

# VARIÁVEIS DE CONFIGURAÇÃO
qtd_carros = 2

if len(sys.argv) != 4:
    print("Número inválido de argumentos. Exatamente 3 argumentos requeridos, na seguinte ordem:" +
        "\n1 - Número total de passageiros\n2 - Capacidade do carro\n3 - Número máximo de passeios")
    os._exit(1)

num_pessoas = None
limite_pessoas_por_carro = None
passeios_por_carro = None

try:
    num_pessoas = int(sys.argv[1])
    limite_pessoas_por_carro = int(sys.argv[2])
    passeios_por_carro = int(sys.argv[3])
except ValueError:
    print("Argumento(s) inválido(s)! Os 3 argumentos enviados necessitam ser do tipo inteiro")
    os._exit(1)    

if (num_pessoas < limite_pessoas_por_carro):
    print("Erro! Número total de pessoas/passageiros é menor que a capacidade do carro")
    os._exit(1)

#inicializa carros
first_car_lk = Lock()
first_car_cv = Condition(first_car_lk)
carros = []
carros.append(Carro(limite_pessoas_por_carro, passeios_por_carro, False)) #sets first car
for i in range(qtd_carros - 1):
	carros.append(Carro(limite_pessoas_por_carro, passeios_por_carro, True))
	carros[i].set_prv_car = carros[i + 1]
#finishes setting first car
carros[0].set_prv_car = carros[qtd_carros - 1]

#defines first current car (car to be boarded)
curr_car = carros[0] #global

#Starts all threads
for i in range(qtd_carros):
	carros[i].thread_main.start()


passageiros = []
for x in range(num_pessoas):
    passageiros.append(Passageiro())