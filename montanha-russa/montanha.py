import threading, logging, time
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
    # l.addHandler(streamHandler)


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
        # self.thread_main = Thread(target=self.main)
        self.thread_run = Thread(target=self.run)
        # self.thread_wait_board = Thread(target=self.wait_board)
        # self.thread_wait_unboard = Thread(target=self.wait_unboard)

        # self.unboard = Event()

        self.controller()

    def controller(self):
        for x in range(self.num_passeios):
            print_log("O carro irá fazer o passeio " + str(x + 1))
            self.thread_main.start()

    def main(self):
            self.load()
            self.thread_wait_board.start()
            self.thread_wait_board.join()
            self.unload()
            self.thread_wait_unboard.start()
            self.thread_wait_unboard.join()
            # self.wait_unboard()

    def run(self):
        print_log("Thread do carro iniciada")
        self.boardable.clear()
        self.unboardable.clear()
        tempo = randrange(5) + 1
        print_log("Carro: " + str(self) + " vai andar por " + str(tempo) + " segundos.")
        time.sleep(tempo)

    def wait_board(self):
        while len(self.passageiros) != self.limite_pessoas:
            pass
        self.thread_run.start()
        self.thread_run.join()

    def wait_unboard(self):
        while len(self.passageiros) != 0:
            pass

    def load(self):
        print_log("O embarque do carro está liberado!")
        self.boardable.set()

    def unload(self):
        print_log("O desembarque do carro está liberado!")
        self.unboardable.set()

    def board(self, passageiro):
        if not self.boardable.is_set():
            raise Erro("Carro não liberado para embarque!")
        if len(self.passageiros) >= self.limite_pessoas:
            # self.boardable.clear()
            raise Erro("Carro cheio!")
        self.passageiros.append(passageiro)
        # if len(self.passageiros) == self.limite_pessoas:
        #     self.thread.start()

    def unboard(self, passageiro):
        if not self.unboardable:
            raise Erro("Carro não liberado para desembarque!")
        self.passageiros.remove(passageiro)


class Passageiro(object):
    """Passageiros de uma montanha russa"""

    id_passageiro = 1

    def __init__(self, carro):
        """Constructor for Passageiro"""
        self.id_passageiro = Passageiro.id_passageiro
        Passageiro.id_passageiro += 1
        self.carro = carro
        self.thread = Thread(target=self.run)

    def run(self):
        while True:
            self.board()
            self.unboard()
            self.passear()

    def passear(self):
        tempo = randrange(5)+1
        print_log("Passageiro: "+str(self)+" vai passear no parque por "+str(tempo)+" segundos.")
        time.sleep(tempo)

    def board(self):
        print_log("Passageiro: " +str(self)+" vai tentar entrar no carro")
        if not self.carro.boardable.is_set():
            self.carro.boardable.wait()
        try:
            self.carro.board(self)
            print_log("Passageiro: " + str(self) + " entrou no carro!")
            self.carro.thread_wait_board.join()
            self.carro.thread_run.join()
        except Erro as e:
            print_log("Passageiro: "+str(self)+" não entrou no carro! "+e.msg+" Passageiro vai esperar 1 segundo e tentar novamente!")
            time.sleep(1)
            self.board()

    def unboard(self):
        print_log("Passageiro: "+str(self)+" vai tentar sair do carro")
        if not self.carro.unboardable.is_set():
            self.carro.unboardable.wait()
        try:
            self.carro.unboard(self)
            print_log("Passageiro: " + str(self) + " saiu do carro!")
        except Erro as e:
            print_log("Passageiro: "+str(self)+" não saiu do carro! "+e.msg+" Passageiro vai esperar 1 segundo e tentar novamente!")
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

for passageiro in passageiros:
    passageiro.thread.start()


# handle_carro.join()

# t = Thread(name='car', target=car, args=('test',))
# threads.append(t)
# t.start()
#
# for thread in threads:
#     thread.join()
