from web_server import web_server
import time
import logging


logger = logging.getLogger('root')
while True:
    try:
        web_server.run()
    except Exception as ex:
        logger.exception("CRIT IN WEB SERVER: {}".format(ex))
