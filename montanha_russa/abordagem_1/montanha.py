import os
import sys
import time
from random import randrange
from threading import Thread, Event, BoundedSemaphore

from montanha_russa.logger import print_carro_log, print_passageiros_log

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


class Carro(object):
    """Carro de uma montanha russa"""

    def __init__(self, limite_passageiros, num_passeios):
        """Constructor for Car"""
        # variáveis para controle de passageiros/assentos
        self.num_passeios = num_passeios
        self.limite_passageiros = limite_passageiros
        self.passageiros = 0
        self.assentos = BoundedSemaphore(value=self.limite_passageiros)

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

            print_carro_log("Carro: " + str(self) + " espera terminar o passaio para liberar desembarque!")
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
            self.boardable.clear()
            self.cheio.set()

    def unboard(self):
        self.cheio.clear()
        self.passageiros -= 1
        if self.passageiros == 0:
            self.unboardable.clear()
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
