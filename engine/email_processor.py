import logging
import sqlite3
import sender
import reader
import time
import threading

DB_PATH = 'db.sqlite'


_connection = sqlite3.connect(DB_PATH)


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


_connection.row_factory = _dict_factory
_cursor = _connection.cursor()


_encode_str = {
    "'": "SINGLE_QUOTE",
    '"': "DOUBLE_QUOTE",
}

_decode_str = {
    "SINGLE_QUOTE": "'",
    "DOUBLE_QUOTE": '"',
}


def _encode(s):
    for key in _encode_str:
        s = s.replace(key, _encode_str[key])
    return s


def _decode(s):
    for key in _decode_str:
        s = s.replace(key, _decode_str[key])
    return s


def poll():
    while True:
        current_time = int(time.time())
        _cursor.execute('SELECT id,token,to_addr,html_text,subject,unsubscribe_link,image_file,login,password,server,ts FROM queue WHERE ts<{}'.format(current_time))  # noqa
        emails = _cursor.fetchall()
        logging.info('[poll] Emails to send: {}'.format(len(emails)))
        threads = []
        for email in emails:
            tr = threading.Thread(
                target=sender.send_email,
                kwargs={
                    'login': email['login'],
                    'password': email['password'],
                    'server': email['server'],
                    'to_addr': email['to_addr'],
                    'html_text': _decode(email['html_text']),
                    'subject': _decode(email['subject']),
                    'unsubscribe_link': email['unsubscribe_link'],
                    'testing': False,
                }
            )
            tr.run()
            threads.append(tr)
        while threads:
            for tr in threads:
                if not tr.isAlive():
                    threads.remove(tr)
        for email in emails:
            _cursor.execute(
                'DELETE FROM queue WHERE id={}'.format(email['id'])
            )
        _connection.commit()
        time.sleep(0.1)


def schedule(
        token,
        login,
        password,
        server,
        spreadsheet_link,
        delay=5,
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    data = reader.get_default_values_from_spreadsheet(
        _get_spreadsheet_id(spreadsheet_link)
    )
    current_time = int(time.time())
    for item in data:
        cursor.execute(
            '''
                INSERT INTO queue(login, password, server, to_addr, html_text, subject, unsubscribe_link, ts, token)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',  # noqa
            [
                login,
                password,
                server,
                item['to_addr'],
                _encode(item['html_text']),
                _encode(item['subject']),
                item['unsubscribe_link'],
                current_time,
                token
            ]
        )
        current_time += delay
    connection.commit()


def _get_spreadsheet_id(spreadsheet_link):
    found = False
    for s in spreadsheet_link.split('/'):
        if found:
            return s
        if s == 'd':
            found = True
    return ''


def get_progress(login):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(login) FROM queue WHERE login=?', [login])
    count = cursor.fetchall()[0][0]
    connection.close()
    return count
