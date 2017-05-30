import time
import os
import sys
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

setup_logger("banheiro_log", "banheiro.log")
banheiro_log = getLogger("banheiro_log")

setup_logger("pessoas_log", "pessoas.log")
pessoas_log = getLogger("pessoas_log")


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


# VARIÁVEIS DE CONFIGURAÇÃO
limite_pessoas = 3


class Banheiro(object):
    """Implementação de um banheiro"""
# TODO documentar variáveis

    def __init__(self, limite_pessoas):
        """Constructor for Banheiro"""
        # variaaves
        self.limite_pessoas = limite_pessoas
        self.pessoas = 0
        self.vagas = BoundedSemaphore(value=self.limite_pessoas)
        self.limite_swap = 2*limite_pessoas
        self.swap_atual = 0

        # variaaves
        self.masculino = Event()
        self.feminino = Event()
        # variaaves
        self.tornar_unissex()

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

banheiro = Banheiro(qt_vagas_banheiro)

pessoas = []
for x in range(qt_homens):
    pessoas.append(Pessoa('M', banheiro))

for x in range(qt_mulheres):
    pessoas.append(Pessoa('F', banheiro))

time.sleep(100)
os._exit(1)
