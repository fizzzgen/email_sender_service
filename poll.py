import logging
from engine import email_processor

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/engine.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

while True:
    try:
        email_processor.poll()
    except Exception as ex:
        logger.exception("CRIT IN ENGINE: {}".format(ex))
