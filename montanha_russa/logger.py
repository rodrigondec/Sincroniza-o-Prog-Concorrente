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
