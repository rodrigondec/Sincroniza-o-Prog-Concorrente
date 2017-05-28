import logging
import time
import os
from random import randrange
from threading import Thread, Event, BoundedSemaphore


# VARIÁVEIS DE CONFIGURAÇÃO
num_pessoas = 12
limite_pessoas_por_carro = 6
passeios_por_carro = 3


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


class Carro(object):
    """Carro de uma montanha russa"""

    def __init__(self, limite_passageiros, num_passeios):
        """Constructor for Car"""

        self.num_passeios = num_passeios
        self.limite_passageiros = limite_passageiros
        self.passageiros = 0
        self.assentos = BoundedSemaphore(value=self.limite_passageiros)
        self.boardable = Event()
        self.unboardable = Event()
        self.cheio = Event()
        self.vazio = Event()
        self.thread_main = Thread(target=self.main)
        self.boardable.clear()
        self.unboardable.clear()
        self.cheio.clear()
        self.vazio.set()

        self.thread_main.start()

    def main(self):
        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " passeio nº " + str(x + 1))

            print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar o embarque!")
            if not self.vazio.is_set():
                self.vazio.wait()

            self.load()
            print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
            if not self.cheio.is_set():
                self.cheio.wait()

            self.run()

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
        self.unboardable.clear()
        self.boardable.set()

    def unload(self):
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.boardable.clear()
        self.unboardable.set()

    def board(self):
        self.vazio.clear()
        self.passageiros += 1
        if self.passageiros == self.limite_passageiros:
            self.cheio.set()

    def unboard(self):
        self.cheio.clear()
        self.passageiros -= 1
        if self.passageiros == 0:
            self.vazio.set()


class Passageiro(object):
    """Passageiros de uma montanha russa"""

    id_passageiro = 1

    def __init__(self, carro):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        Passageiro.id_passageiro += 1
        self.carro = carro
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            print_passageiros_log("Passageiro: " + str(self) + " pergunta: é minha vez?")
            with self.carro.assentos:
                print_passageiros_log("Passageiro: " + str(self) + " irá poder entrar no carro!")
                self.board()
                self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_passageiros_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos!")
        time.sleep(tempo)

    def board(self):
        print_passageiros_log("Passageiro: " + str(self) + " pergunta: embarque do carro está liberado?")
        if not self.carro.boardable.is_set():
            self.carro.boardable.wait()
        print_passageiros_log("Passageiro: " + str(self) + " entrou no carro!")
        self.carro.board()

    def unboard(self):
        print_passageiros_log("Passageiro: " + str(self) + " pergunta: desembarque do carro está liberado?")
        if not self.carro.unboardable.is_set():
            self.carro.unboardable.wait()
        print_passageiros_log("Passageiro: "+str(self)+" saiu do carro!")
        self.carro.unboard()

    def __str__(self):
        return str(self.id_passageiro)


carro = Carro(limite_pessoas_por_carro, passeios_por_carro)

passageiros = []

for x in range(8):
    passageiros.append(Passageiro(carro))