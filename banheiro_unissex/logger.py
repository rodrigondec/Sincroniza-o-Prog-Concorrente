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
