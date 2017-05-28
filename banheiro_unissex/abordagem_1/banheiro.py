import logging
import time
from random import randrange
from threading import Thread, Event, BoundedSemaphore


# VARIÁVEIS DE CONFIGURAÇÃO
limite_pessoas = 3


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

    def __init__(self, limite_pessoas):
        """Constructor for Banheiro"""

        self.limite_pessoas = limite_pessoas
        self.pessoas = 0
        self.vagas = BoundedSemaphore(value=self.limite_pessoas)
        self.limite_swap = 2*limite_pessoas
        self.swap_atual = 0
        self.masculino = Event()
        self.feminino = Event()

        self.masculino.set()
        self.feminino.set()

    def swap(self):
        self.swap_atual += 1
        if self.swap_atual%self.limite_swap == 0:
            self.swap_atual = 0
            if self.masculino.is_set():
                print_banheiro_log("Banheiro: foi masulino por muito tempo!!!!")
                self.tornar_feminino()
            if self.feminino.is_set():
                print_banheiro_log("Banheiro: foi feminino por muito tempo!!!!")
                self.tornar_masculino()

    def tornar_feminino(self):
        self.feminino.set()
        self.masculino.clear()
        print_banheiro_log("Banheiro: é feminino agora!")

    def tornar_masculino(self):
        self.feminino.clear()
        self.masculino.set()
        print_banheiro_log("Banheiro: é masculino agora!")

    def tornar_unissex(self):
        self.masculino.set()
        self.feminino.set()
        print_banheiro_log("Banheiro: é unissex agora!")

    def entrar(self):
        if self.pessoas == 0:
            self.swap_atual = 0
            # if sexo == 'F':
            #     self.feminino()
            #     self.swap_atual = 0
            # elif sexo == 'M':
            #     self.masculino()
            #     self.swap_atual = 0

        self.pessoas += 1

        print_banheiro_log("Banheiro: tem "+str(self.pessoas)+" pessoa(s) no banheiro")

        self.swap()

    def sair(self):
        self.pessoas -= 1

        print_banheiro_log("Banheiro: tem "+str(self.pessoas)+" pessoa(s) no banheiro")

        if self.pessoas == 0:
            self.swap_atual = 0
            self.tornar_unissex()


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

        self.thread.start()

    def run(self):
        while True:
            self.trabalhar()
            self.esperar_genero()
            print_pessoas_log("Pessoa: " + str(self) + " pergunta: é minha vez?")
            with banheiro.vagas:
                self.entrar()
                self.sair()

    def trabalhar(self):
        tempo = randrange(10) + 10
        print_pessoas_log("Pessoa: "+str(self)+" vai trabalhar por "+str(tempo)+" segundos.")
        time.sleep(tempo)

    def esperar_genero(self):
        if self.sexo == 'M':
            print_pessoas_log("Pessoa: " + str(self) + " pergunta: o banheiro é masculino?")
            if not self.banheiro.masculino.is_set():
                self.banheiro.masculino.wait()
            self.banheiro.tornar_masculino()
        elif self.sexo == 'F':
            print_pessoas_log("Pessoa: " + str(self) + " pergunta: o banheiro é feminino?")
            if not self.banheiro.feminino.is_set():
                self.banheiro.feminino.wait()
            self.banheiro.tornar_feminino()

    def entrar(self):
        print_pessoas_log("Pessoa: " + str(self) + " entrou no banheiro!")
        self.banheiro.entrar()

        tempo = randrange(5) + 1
        print_pessoas_log("Pessoa: " + str(self) + " vai ficar no banheiro por " + str(tempo) + " segundos.")
        time.sleep(tempo)

    def sair(self):
        print_pessoas_log("Pessoa: "+str(self)+" saiu do banheiro")
        self.banheiro.sair()

    def __str__(self):
        return str(self.id_pessoa)+" ("+self.sexo+")"

banheiro = Banheiro(limite_pessoas)

pessoas = []

for x in range(5):
    pessoas.append(Pessoa('M', banheiro))
    pessoas.append(Pessoa('F', banheiro))
