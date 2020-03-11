from engine import email_processor
import logging
logging.basicConfig(filename='log', force=True)


email_processor.poll()
