import threading, logging, time
from random import randrange
from threading import Thread, Event


def car():
    pass


def passenger():
    pass


threads = []

t = Thread(name='car', target=car, args=('test',))
threads.append(t)
t.start()

for thread in threads:
    thread.join()
