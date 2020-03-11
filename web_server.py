from web_server import web_server
import logging
logging.basicConfig(filename='logs/web_server.log', force=True)


web_server.run()
