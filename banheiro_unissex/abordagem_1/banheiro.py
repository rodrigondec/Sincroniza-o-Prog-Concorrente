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

setup_logger("fila_log", "fila.log")
fila_log = getLogger("fila_log")


def print_info_log(msg):
    info_log.info(msg)


def print_banheiro_log(msg):
    print(msg)
    banheiro_log.info(msg)
    print_info_log(msg)


def print_fila_log(msg):
    print(msg)
    fila_log.info(msg)
    print_info_log(msg)


def print_pessoas_log(msg):
    print(msg)
    pessoas_log.info(msg)
    print_info_log(msg)


class Banheiro(object):
    """Implementação de um banheiro"""

    id_banheiro = 1

    def __init__(self, limite_pessoas):
        """Constructor for Banheiro"""
        self.id_banheiro = Banheiro.id_banheiro
        Banheiro.id_banheiro += 1

        # controle de pessoas no banheiro
        self.limite_pessoas = limite_pessoas
        self.pessoas = 0
        self.vagas = BoundedSemaphore(value=self.limite_pessoas)

        # situações do banheiro
        self.disponivel = Event()
        self.vazio = Event()
        self.disponivel.set()
        self.vazio.set()

        # controle das filas do banheiro
        self.pessoa_atual = None
        self.fila = None

        self.fila_masculino = Queue()
        self.fila_feminino = Queue()

        # controle de gênero do banheiro
        self.masculino = Event()
        self.feminino = Event()

        # banheiro começa masculino
        self.tornar_masculino()

        self.thread_fila = Thread(target=self.controlar_fila)
        self.thread_fila.start()

    def trocar_genero(self):
        print_banheiro_log("Banheiro: " + str(self) + " vai trocar o gênero. Espera estar vazio!")
        if not self.vazio.is_set():
            self.vazio.wait()

        if self.masculino.is_set():
            self.tornar_feminino()
        elif self.feminino.is_set():
            self.tornar_masculino()

    def controlar_fila(self):
        while True:
            if self.masculino.is_set():
                print_fila_log("fila: " + str(self) + " banheiro é masculino!")
            elif self.feminino.is_set():
                print_fila_log("fila: " + str(self) + " o banheiro é feminino!")
            print_fila_log("fila: " + str(self) + " tem "+str(self.fila_masculino.qsize())+" homens na fila masculina!")
            print_fila_log("fila: " + str(self) + " tem "+str(self.fila_feminino.qsize())+" mulheres na fila feminina!")

            if (self.fila_masculino.qsize() > (self.fila_feminino.qsize()+(int(1.5*self.limite_pessoas))) or
                    self.fila_feminino.qsize() > (self.fila_masculino.qsize()+(int(1.5*self.limite_pessoas))) or
                    self.fila_feminino.empty() and not self.fila_masculino.empty() or
                    self.fila_masculino.empty() and not self.fila_feminino.empty()):
                self.trocar_genero()

            if not self.disponivel.is_set():
                print_fila_log("fila: " + str(self) + " espera estar disponível para liberar a fila!")
                self.disponivel.wait()

            self.pessoa_atual = self.fila.get()
            print_fila_log("fila: " + str(self) + " é a vez da pessoa "+str(self.pessoa_atual))
            self.pessoa_atual.vez.set()

            print_fila_log("fila: " + str(self) + " espera a pessoa "+str(self.pessoa_atual)+" entrar no banheiro!")
            if not self.pessoa_atual.entrou.is_set():
                self.pessoa_atual.entrou.wait()

            self.pessoa_atual.vez.clear()

    def tornar_feminino(self):
        self.feminino.set()
        self.masculino.clear()
        self.fila = self.fila_feminino
        print_banheiro_log("Banheiro: se tornou feminino agora!")

    def tornar_masculino(self):
        self.feminino.clear()
        self.masculino.set()
        self.fila = self.fila_masculino
        print_banheiro_log("Banheiro: se tornou masculino agora!")

    def entrar_fila(self, pessoa):
        if pessoa.sexo == 'M':
            self.fila_masculino.put(pessoa)
        elif pessoa.sexo == 'F':
            self.fila_feminino.put(pessoa)

    def entrar(self):
        # if self.pessoas == 0:
        #     self.swap_atual = 0

        self.pessoas += 1
        self.vazio.clear()
        if self.pessoas == self.limite_pessoas:
            self.disponivel.clear()
        print_banheiro_log("Banheiro: tem "+str(self.pessoas)+" pessoa(s) no banheiro")

        # self.swap()

    def sair(self):
        self.pessoas -= 1
        self.disponivel.set()
        print_banheiro_log("Banheiro: tem "+str(self.pessoas)+" pessoa(s) no banheiro")

        if self.pessoas == 0:
            self.vazio.set()
            # self.swap_atual = 0
            # self.tornar_unissex()

    def __str__(self):
        return str(self.id_banheiro)


class Pessoa(object):
    """Implementação de um banheiro"""

    id_pessoa = 1

    def __init__(self, sexo, banheiro):
        """Constructor for Pessoa"""

        self.id_pessoa = Pessoa.id_pessoa
        Pessoa.id_pessoa += 1

        self.sexo = sexo
        self.banheiro = banheiro

        # controle de situações da pessoa
        self.vez = Event()
        self.entrou = Event()
        self.vez.clear()
        self.entrou.clear()

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            self.trabalhar()

            print_pessoas_log("Pessoa: " + str(self) + " entra na fila!")
            self.banheiro.entrar_fila(self)

            print_pessoas_log("Pessoa: " + str(self) + " pergunta: é minha vez?")
            if not self.vez.is_set():
                self.vez.wait()

            print_pessoas_log("Pessoa: " + str(self) + " vai tentrar entrar no banheiro")
            with banheiro.vagas:
                self.entrar()
                self.sair()

    def trabalhar(self):
        tempo = randrange(10) + 10
        print_pessoas_log("Pessoa: "+str(self)+" vai trabalhar por "+str(tempo)+" segundos.")
        time.sleep(tempo)

    def entrar(self):
        print_pessoas_log("Pessoa: " + str(self) + " entrou no banheiro!")
        self.banheiro.entrar()
        self.entrou.set()
        tempo = randrange(5) + 1
        print_pessoas_log("Pessoa: " + str(self) + " vai ficar no banheiro por " + str(tempo) + " segundos.")
        time.sleep(tempo)

    def sair(self):
        print_pessoas_log("Pessoa: "+str(self)+" saiu do banheiro")
        self.banheiro.sair()
        self.entrou.clear()

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
