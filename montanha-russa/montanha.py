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


setup_logger("log", "info.log")
log = logging.getLogger("log")

def print_log(msg):
    print(msg)
    log.info(msg)

class Erro(Exception):
    def __init__(self, msg):
        self.msg = msg

