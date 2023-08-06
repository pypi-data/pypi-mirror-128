import logging
import sys

def logger_setup():
    log_filename = 'execution.log'
    logger = logging.getLogger(__name__)

    if not logger.handlers:
        fhandler = logging.FileHandler(filename=log_filename, mode='w')
        formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(logging.DEBUG)
    return logger


