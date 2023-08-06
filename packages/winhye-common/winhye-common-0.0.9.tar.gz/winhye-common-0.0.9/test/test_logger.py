import os
import sys
import time

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(PATH)
print(PATH)

from src.winhye_common.winhye_logger import logging as logging


def log_test():
    logger = logging.getLogger()
    for i in range(10000):
        logger.info("1111111111111111")
        time.sleep(1)


def log_test2():
    logger = logging.getLogger()
    logger.report("123456")


def log_test3():
    logger = logging.getLogger()
    logger.debug('11111111')
    logger.info('222222222')
    logger.warning('33333333')
    logger.error('4444444')


if __name__ == '__main__':
    log_test3()
