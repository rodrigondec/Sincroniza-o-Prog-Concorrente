import os
import sys
import time
from random import randrange
from threading import Thread, Event, BoundedSemaphore
from queue import Queue
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


class Carro(object):
    """Carro de uma montanha russa"""

    id_carro = 1

    def __init__(self, limite_passageiros, num_passeios):
        """Constructor for Car"""
        self.id_carro = Carro.id_carro
        Carro.id_carro += 1

        # variáveis para controle de passageiros/assentos
        self.num_passeios = num_passeios
        self.limite_passageiros = limite_passageiros
        self.passageiros = 0
        self.assentos = BoundedSemaphore(value=self.limite_passageiros)

        self.passageiro_atual = None
        self.fila = Queue()

        # variáveis para controle de eventos/situações
        self.boardable = Event()
        self.unboardable = Event()
        self.cheio = Event()
        self.vazio = Event()
        # carro começa com embarque e desembarque bloqueados
        self.boardable.clear()
        self.unboardable.clear()
        # carro começa vazio
        self.cheio.clear()
        self.vazio.set()

        # thread de controle do carro
        self.thread_main = Thread(target=self.main)
        self.thread_main.start()

        self.thread_fila = Thread(target=self.controlar_fila)
        self.thread_fila.start()

    def main(self):
        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " passeio nº " + str(x + 1))

            self.unload()
            print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar o embarque!")
            if not self.vazio.is_set():
                self.vazio.wait()

            self.load()
            print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
            if not self.cheio.is_set():
                self.cheio.wait()

            print_carro_log("Carro: " + str(self) + " espera terminar o passaio para liberar desembarque!")
            self.run()

        os._exit(1)

    def controlar_fila(self):
        while True:
            print_carro_log("Carro/fila: " + str(self) + " espera estar em embarque para liberar a fila!")
            if not self.boardable.is_set():
                self.boardable.wait()
            self.passageiro_atual = self.fila.get()
            print_carro_log("Carro/fila: " + str(self) + " é a vez do passageiro "+str(self.passageiro_atual))
            self.passageiro_atual.vez.set()
            print_carro_log("Carro/fila: " + str(self) + " espera o passageiro "+str(self.passageiro_atual)+" entrar no carro!")
            if not self.passageiro_atual.boarded.is_set():
                self.passageiro_atual.boarded.wait()
            self.passageiro_atual.vez.clear()

    def run(self):
        self.boardable.clear()
        self.unboardable.clear()
        print_carro_log("Carro: " + str(self) + " passeio iniciado!")
        tempo = randrange(5) + 1
        print_carro_log("Carro: " + str(self) + " vai andar por " + str(tempo) + " segundos.")
        time.sleep(tempo)
        print_carro_log("Carro: " + str(self) + " passeio terminado!")

    def load(self):
        print_carro_log("Carro: " + str(self) + " embarque do carro está liberado!")
        self.unboardable.clear()
        self.boardable.set()

    def unload(self):
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.boardable.clear()
        self.unboardable.set()

    def entrar_fila(self, passageiro):
        self.fila.put(passageiro)

    def board(self):
        self.vazio.clear()
        self.passageiros += 1
        if self.passageiros == self.limite_passageiros:
            self.boardable.clear()
            self.cheio.set()

    def unboard(self):
        self.cheio.clear()
        self.passageiros -= 1
        if self.passageiros == 0:
            self.unboardable.clear()
            self.vazio.set()

    def __str__(self):
        return str(self.id_carro)


class Passageiro(object):
    """Passageiros de uma montanha russa"""

    id_passageiro = 1

    def __init__(self, carro):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        Passageiro.id_passageiro += 1

        self.carro = carro

        self.vez = Event()
        self.boarded = Event()

        self.vez.clear()
        self.boarded.clear()

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            print_passageiros_log("Passageiro: " + str(self) + " entra na fila!")
            self.carro.entrar_fila(self)
            print_passageiros_log("Passageiro: " + str(self) + " pergunta: é minha vez?")
            if not self.vez.is_set():
                self.vez.wait()
            print_passageiros_log("Passageiro: " + str(self) + " vai tentar entrar no carro!")
            with self.carro.assentos:
                self.board()
                self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_passageiros_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos!")
        time.sleep(tempo)

    def board(self):
        print_passageiros_log("Passageiro: " + str(self) + " entrou no carro!")
        self.carro.board()
        self.boarded.set()

    def unboard(self):
        print_passageiros_log("Passageiro: " + str(self) + " pergunta: desembarque do carro está liberado?")
        if not self.carro.unboardable.is_set():
            self.carro.unboardable.wait()
        print_passageiros_log("Passageiro: "+str(self)+" saiu do carro!")
        self.carro.unboard()
        self.boarded.clear()

    def __str__(self):
        return str(self.id_passageiro)


# VARIÁVEIS DE CONFIGURAÇÃO
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

if num_pessoas < limite_pessoas_por_carro:
    print("Erro! Número total de pessoas/passageiros é menor que a capacidade do carro")
    os._exit(1)

carro = Carro(limite_pessoas_por_carro, passeios_por_carro)

passageiros = []
for x in range(num_pessoas):
    passageiros.append(Passageiro(carro))
