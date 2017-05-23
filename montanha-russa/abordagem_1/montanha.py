import logging
import time
import os
from random import randrange
from threading import Thread, Event


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

    def __init__(self, limite_pessoas, num_passeios, passageiros=None):
        """Constructor for Car"""
        self.limite_pessoas = limite_pessoas
        self.num_passeios = num_passeios
        if passageiros is None:
            passageiros = []
        self.passageiros = passageiros
        self.boardable = Event()
        self.unboardable = Event()
        self.cheio = Event()
        self.vazio = Event()
        self.thread_main = Thread(target=self.main)
        self.thread_run = Thread(target=self.run)
        self.boardable.clear()
        self.unboardable.clear()
        self.cheio.clear()
        self.vazio.set()
        self.thread_main.start()

    def main(self):
        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " irá fazer o passeio " + str(x + 1))
            print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar embarque!")
            if not self.vazio.is_set():
                self.vazio.wait()
            self.load()
            print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
            if not self.cheio.is_set():
                self.cheio.wait()
            self.thread_run = Thread(target=self.run)
            self.thread_run.start()
            print_carro_log("Carro: " + str(self) + " espera terminar o passaio para liberar desembarque!")
            self.thread_run.join()
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
        self.boardable.set()

    def unload(self):
        print_carro_log("Carro: " + str(self) + " desembarque do carro está liberado!")
        self.unboardable.set()

    def board(self, passageiro):
        if not self.boardable.is_set():
            raise Erro("Carro não liberado para embarque!")
        if len(self.passageiros) >= self.limite_pessoas:
            raise Erro("Carro cheio!")
        self.passageiros.append(passageiro)
        if len(self.passageiros) == self.limite_pessoas:
            self.boardable.clear()
            self.vazio.clear()
            self.cheio.set()

    def unboard(self, passageiro):
        if not self.unboardable:
            raise Erro("Carro não liberado para desembarque!")
        self.passageiros.remove(passageiro)
        if len(self.passageiros) == 0:
            self.unboardable.clear()
            self.cheio.clear()
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
            self.board()
            self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_passageiros_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos.")
        time.sleep(tempo)

    def board(self):
        print_passageiros_log("Passageiro: " + str(self) + " espera poder entrar no carro")
        if not self.carro.boardable.is_set():
            self.carro.boardable.wait()
        print_passageiros_log("Passageiro: " +str(self)+" vai tentar entrar no carro")
        try:
            self.carro.board(self)
            print_passageiros_log("Passageiro: " + str(self) + " entrou no carro!")
        except Erro as e:
            print_passageiros_log("Passageiro: "+str(self)+" não entrou no carro! "+e.msg+" Passageiro vai esperar 1 segundo e tentar novamente!")
            time.sleep(1)
            self.board()

    def unboard(self):
        print_passageiros_log("Passageiro: " + str(self) + " espera poder sair do carro")
        if not self.carro.unboardable.is_set():
            self.carro.unboardable.wait()
        print_passageiros_log("Passageiro: "+str(self)+" vai tentar sair do carro")
        try:
            self.carro.unboard(self)
            print_passageiros_log("Passageiro: " + str(self) + " saiu do carro!")
        except Erro as e:
            print_passageiros_log("Passageiro: "+str(self)+" não saiu do carro! "+e.msg+" Passageiro vai esperar 1 segundo e tentar novamente!")
            time.sleep(1)
            self.unboard()

    def __str__(self):
        return str(self.id_passageiro)


num_pessoas = 8
limite_pessoas_por_carro = 6
passeios_por_carro = 3

carro = Carro(limite_pessoas_por_carro, passeios_por_carro)

passageiros = []

for x in range(8):
    passageiros.append(Passageiro(carro))