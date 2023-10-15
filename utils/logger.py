import logging

# TODO migrate to .env file
LOG_LEVEL = 'INFO'

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)


def custom_logger(n=__name__):
    logger = logging.getLogger(n)
    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = 0
    return logger
