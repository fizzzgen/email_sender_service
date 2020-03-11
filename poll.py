from engine import email_processor
import logging
logging.basicConfig(filename='logs/engine.log', force=True)


email_processor.poll()
