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

setup_logger("banheiro_log", "banheiro.log")
banheiro_log = logging.getLogger("banheiro_log")

setup_logger("pessoas_log", "pessoas.log")
pessoas_log = logging.getLogger("pessoas_log")


def print_info_log(msg):
    info_log.info(msg)


def print_banheiro_log(msg):
    print(msg)
    banheiro_log.info(msg)
    print_info_log(msg)


def print_pessoas_log(msg):
    print(msg)
    pessoas_log.info(msg)
    print_info_log(msg)


class Erro(Exception):
    def __init__(self, msg):
        self.msg = msg


class Banheiro(object):
    """Implementação de um banheiro"""

    def __init__(self, limite_pessoas, pessoas=None):
        """Constructor for Banheiro"""
        if pessoas is None:
            pessoas = []
        self.limite_pessoas = limite_pessoas
        self.limite_swap = 2*limite_pessoas
        self.swap_atual = 0
        self.pessoas = pessoas
        self.masculino = Event()
        self.feminino = Event()
        self.disponivel = Event()
        # self.sexo_atual = sexo_atual
        # self.thread = Thread(target=run)

        self.disponivel.set()
        self.masculino.set()
        self.feminino.set()

    def swap(self):
        self.swap_atual += 1
        if self.swap_atual%self.limite_swap == 0:
            self.swap_atual = 0
            if self.masculino.is_set():
                self.masculino.clear()
                self.feminino.set()
                print_banheiro_log("Banheiro: é feminino agora")
            if self.feminino.is_set():
                self.feminino.clear()
                self.masculino.set()
                print_banheiro_log("Banheiro: é masculino agora")

    def entrar(self, pessoa):
        if len(self.pessoas) == 0:
            if pessoa.sexo == 'F':
                self.masculino.clear()
                print_banheiro_log("Banheiro: é feminino agora")
                self.swap_atual = 0
            elif pessoa.sexo == 'M':
                self.feminino.clear()
                print_banheiro_log("Banheiro: é masculino agora")
                self.swap_atual = 0
        if len(self.pessoas) >= self.limite_pessoas:
            raise Erro("Banheiro cheio!")
        self.pessoas.append(pessoa)
        print_banheiro_log("Banheiro: pessoa "+str(pessoa)+" entrou no banheiro")
        print_banheiro_log("Banheiro: tem "+str(len(self.pessoas))+" pessoa no banheiro")
        if len(self.pessoas) == self.limite_pessoas:
            self.disponivel.clear()
        self.swap()

    def sair(self, pessoa):
        self.disponivel.set()
        # print_banheiro_log("ERRO: removendo pessoa "+str(pessoa))
        self.pessoas.remove(pessoa)
        print_banheiro_log("Banheiro: pessoa "+str(pessoa)+" saiu do banheiro")
        # print_banheiro_log(self.pessoas)
        print_banheiro_log("Banheiro: tem "+str(len(self.pessoas))+" pessoa no banheiro")
        if len(self.pessoas) == 0:
            print_banheiro_log("Banheiro: é unissex agora")
            self.swap_atual = 0
            self.masculino.set()
            self.feminino.set()


