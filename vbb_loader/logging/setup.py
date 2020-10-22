import logging


def logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)-32s] [%(levelname)-8s] - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
