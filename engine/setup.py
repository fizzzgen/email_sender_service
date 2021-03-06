import sqlite3
import logging

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

logging.info('[setup] Initializing tables...')

try:
    cursor.execute(
        '''
        CREATE TABLE queue(
        id integer primary key autoincrement,
        token TEXT,
        to_addr TEXT,
        html_text TEXT,
        subject TEXT,
        unsubscribe_link TEXT,
        image_file TEXT,
        login TEXT,
        password TEXT,
        server TEXT,
        ts INTEGER,
        status TEXT
        )
        '''
    )
except Exception as e:
    logging.warning(e)
    pass

try:
    cursor.execute('CREATE TABLE token(token TEXT, type TEXT, value INTEGER)')
except Exception as e:
    logging.warning(e)
    pass

connection.commit()
logging.info('[setup] Tables initialized')
