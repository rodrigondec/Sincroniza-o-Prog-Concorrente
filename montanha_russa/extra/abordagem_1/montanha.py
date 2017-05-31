import os
import sys
import time
from queue import Queue, Empty
from random import randrange
from threading import Thread, Event, BoundedSemaphore
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

setup_logger("plataforma_log", "plataforma.log")
plataforma_log = getLogger("plataforma_log")

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


def print_plataforma_log(msg):
    print(msg)
    plataforma_log.info(msg)
    print_info_log(msg)


"""
Essa abordagem irá fazer o uso de eventos e semáforos. Os eventos são utilizados para controlar as fases de
embarque e desembarque do veículo e as situações cheio e vazio. O controle do acesso aos assentos do carro é 
feito por um semáforo. 

Considere o caso em que o caro possui 6 vagas mas há 12 pessoas no parque. 
O carro espera o evento vazio para liberar o embarque. 
O carro espera o evento cheio para terminar o embarque e iniciar o passeio. 
Depois do passeio, é iniciado o desembarque.

Os passageiros tentam alocar um assento do semáforo, com isso fazendo o controle de limite de pessoas no carro. 
Depois de alocar o assento, eles esperam o embarque ser liberado para entrar de fato no carro. 
Após embarcarem, eles esperam o desembarque do carro. Ao desembarcarem, liberam o assento adquirido e vão passear.
"""

class Plataforma(object):
    """Plataforma de carros de uma montanha russa"""

    def __init__(self):
        """Constructor for Plataforma"""

        self.fila_carros = Queue()
        # self.carro_anterior
        self.carro_atual = None

        self.fila_passageiros = Queue()
        self.passageiro_atual = None

        self.tem_carro = Event()
        self.acesso = BoundedSemaphore()

        self.tem_carro.clear()

        self.thread_fila_carros = Thread(target=self.controlador_fila_carros)
        self.thread_fila_carros.start()
        self.thread_fila_passageiros = Thread(target=self.controlador_fila_passageiros)
        self.thread_fila_passageiros.start()

    def controlador_fila_passageiros(self):
        while True:
            if not self.tem_carro.is_set():
                print_plataforma_log("Fila passageiros: espera ter carro na plataforma!")
                self.tem_carro.wait()

            # while true para esperar o carro cheio iniciar seu passeio
            # Sai do while não quando o carro deixa de estar cheio, mas sim quando o carro_atual for trocado
            while self.carro_atual.cheio.is_set():
                pass

            if not self.carro_atual.boardable.is_set():
                print_plataforma_log("Fila passageiros: espera o embarque do carro "+str(self.carro_atual)+" para liberar passageiros!")
                self.carro_atual.boardable.wait()

            self.passageiro_atual = self.fila_passageiros.get()

            print_plataforma_log("Fila passageiros: é a vez do passageiro " + str(self.passageiro_atual) + "!")
            self.passageiro_atual.vez.set()

            if not self.passageiro_atual.boarded.is_set():
                print_plataforma_log("Fila passageiros: espera passageiro "+str(self.passageiro_atual)+" entrar no carro!")
                self.passageiro_atual.boarded.wait()
            self.passageiro_atual.vez.clear()

    def controlador_fila_carros(self):
        try:
            while True:
                self.tem_carro.clear()
                self.carro_atual = self.fila_carros.get(timeout=5)
                self.tem_carro.set()

                if not self.carro_atual.passeio_terminado.is_set():
                    print_plataforma_log("Fila carros: espera o carro "+str(self.carro_atual)+" terminar o passeio!")
                    self.carro_atual.passeio_terminado.wait()

                print_plataforma_log("Fila carros: é a vez do carro "+str(self.carro_atual))
                self.carro_atual.vez.set()

                if not self.carro_atual.passeio_iniciado.is_set():
                    print_plataforma_log("Fila carros: espera o carro "+str(self.carro_atual)+" iniciar seu passeio para liberar o proximo carro!")
                    self.carro_atual.passeio_iniciado.wait()
                    self.carro_atual.passeio_iniciado.clear()

                self.tem_carro.clear()
                self.carro_atual.vez.clear()

                self.entrar_fila_carros(self.carro_atual)
        except Empty:
            print_plataforma_log("Plataforma/fila_carros: terminou todos os passeios!")
            os._exit(1)

    def entrar_fila_passageiros(self, passageiro):
        self.fila_passageiros.put(passageiro)

    def entrar_fila_carros(self, carro):
        self.fila_carros.put(carro)

class Carro(object):
    """Carro de uma montanha russa"""
    id_carro = 1

    def __init__(self, limite_passageiros, num_passeios, plataforma: Plataforma):
        """Constructor for Car"""
        self.id_carro = Carro.id_carro
        Carro.id_carro += 1

        # variáveis para controle de passageiros/assentos
        self.num_passeios = num_passeios
        self.limite_passageiros = limite_passageiros
        self.passageiros = 0
        self.assentos = BoundedSemaphore(value=self.limite_passageiros)

        self.plataforma = plataforma

        # variáveis para controle de eventos/situações
        self.boardable = Event()
        self.unboardable = Event()
        self.cheio = Event()
        self.vazio = Event()
        self.passeio_iniciado = Event()
        self.passeio_terminado = Event()
        self.vez = Event()
        # carro começa com embarque e desembarque bloqueados
        self.boardable.clear()
        self.unboardable.clear()
        # carro começa vazio
        self.cheio.clear()
        self.vazio.set()
        # carro começa zerado
        self.passeio_iniciado.clear()
        self.passeio_terminado.set()
        self.vez.clear()

        # thread de controle do carro
        self.thread_main = Thread(target=self.main)
        self.thread_main.start()

        print_carro_log("Carro: " + str(self) + " entra na fila da plataforma!")
        self.plataforma.entrar_fila_carros(self)

    def main(self):
        for x in range(self.num_passeios):
            print_carro_log("Carro: " + str(self) + " passeio nº " + str(x + 1))

            if not self.vez.is_set():
                print_carro_log("Carro: " + str(self) + " espera sua vez!")
                self.vez.wait()

            print_carro_log("Carro: " + str(self) + " adquire acesso da plataforma!")
            with self.plataforma.acesso:

                self.unload()
                if not self.vazio.is_set():
                    print_carro_log("Carro: " + str(self) + " espera estar vazio para liberar o embarque!")
                    self.vazio.wait()

                self.load()
                if not self.cheio.is_set():
                    print_carro_log("Carro: " + str(self) + " espera estar cheio para iniciar passeio!")
                    self.cheio.wait()

            self.run()
        os._exit(1)

    def run(self):
        self.boardable.clear()
        self.unboardable.clear()
        self.passeio_terminado.clear()
        self.passeio_iniciado.set()
        print_carro_log("Carro: " + str(self) + " passeio iniciado!")
        tempo = 5
        print_carro_log("Carro: " + str(self) + " vai andar por " + str(tempo) + " segundos.")
        time.sleep(tempo)
        print_carro_log("Carro: " + str(self) + " passeio terminado!")
        self.passeio_terminado.set()

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

    def __init__(self, plataforma: Plataforma):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        Passageiro.id_passageiro += 1

        self.plataforma = plataforma
        self.carro_atual = None

        # variáveis para controle de evento/situação
        self.vez = Event()
        self.boarded = Event()
        # passageiro começa zerado
        self.vez.clear()
        self.boarded.clear()

        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            print_passageiros_log("Passageiro: " + str(self) + " entra na fila!")
            self.plataforma.entrar_fila_passageiros(self)

            if not self.vez.is_set():
                print_passageiros_log("Passageiro: " + str(self) + " espera sua vez!")
                self.vez.wait()

            self.carro_atual = self.plataforma.carro_atual

            print_passageiros_log("Passageiro: " + str(self) + " vai tentar entrar no carro " + str(self.carro_atual) + "!")
            with self.carro_atual.assentos:
                self.board()
                self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_passageiros_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos!")
        time.sleep(tempo)

    def board(self):
        print_passageiros_log("Passageiro: " + str(self) + " entrou no carro " + str(self.carro_atual) + "!")
        self.carro_atual.board()
        self.boarded.set()

    def unboard(self):
        print_passageiros_log("Passageiro: " + str(self) + " pergunta: desembarque do carro "+str(self.carro_atual)+" está liberado?")
        if not self.carro_atual.unboardable.is_set():
            self.carro_atual.unboardable.wait()
        print_passageiros_log("Passageiro: " + str(self) + " saiu do carro " + str(self.carro_atual) + "!")
        self.carro_atual.unboard()
        self.boarded.clear()


    def __str__(self):
        return str(self.id_passageiro)


# VARIÁVEIS DE CONFIGURAÇÃO
if len(sys.argv) != 5:
    print("Número inválido de argumentos. Exatamente 3 argumentos requeridos, na seguinte ordem:" +
          "\n1 - Número total de passageiros\n2 - Capacidade do carro\n3 - Número máximo de passeios\n4 - Número de carros")
    os._exit(1)

num_pessoas = None
limite_pessoas_por_carro = None
passeios_por_carro = None
num_carros = None

try:
    num_pessoas = int(sys.argv[1])
    limite_pessoas_por_carro = int(sys.argv[2])
    passeios_por_carro = int(sys.argv[3])
    num_carros = int(sys.argv[4])
except ValueError:
    print("Argumento(s) inválido(s)! Os 4 argumentos enviados necessitam ser do tipo inteiro")
    os._exit(1)

if num_pessoas < limite_pessoas_por_carro:
    print("Erro! Número total de pessoas/passageiros é menor que a capacidade do carro")
    os._exit(1)

plataforma = Plataforma()

carros = []
for x in range(num_carros):
    carros.append(Carro(limite_pessoas_por_carro, passeios_por_carro, plataforma))
    # plataforma.entrar(carros[x])

passageiros = []
for x in range(num_pessoas):
    passageiros.append(Passageiro(plataforma))
