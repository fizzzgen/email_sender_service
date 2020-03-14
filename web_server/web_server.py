from flask import Flask
from datetime import datetime
from engine import email_processor
from flask import request
from flask import render_template
import flask
import sqlite3
import logging

logger = logging.getLogger('root')


app = Flask(__name__, template_folder="static")


@app.route('/')
def ping():
    return render_template('form.html')


@app.route('/schedule/', methods=['POST'])
def schedule():
    if request.method == 'POST':
        try:
            data = request.form
            token = data['token']
            login = data['login']
            password = data['password']
            server = data['server']
            spreadsheet_link = data['spreadsheet_link']

            email_processor.schedule(
                token,
                login,
                password,
                server,
                spreadsheet_link
            )
        except Exception as ex:
            logger.exception(ex)
            return render_template('form.html', status='EXCEPTION')
        return render_template('form.html', status='SUCCESS')


@app.route('/progress/', methods=['POST', 'GET'])
def progress():
    if request.method == 'POST':
        try:
            data = request.form
            token = data['token']
            conn = sqlite3.connect('db.sqlite')
            cur = conn.cursor()
            cur.execute(
                "SELECT login, to_addr, status, ts FROM queue WHERE token=? ORDER BY ts", (token,)  # noqa
            )
            data = [
                [
                    row[0],
                    row[1],
                    row[2],
                    datetime.utcfromtimestamp(row[3]).strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                ]
                for row in cur.fetchall()
            ]

        except Exception as ex:
            logger.exception(ex)
            return render_template('progress.html', status=repr(ex))
        return render_template('progress.html', progress=data)
    if request.method == 'GET':
        return render_template('progress.html')


@app.route('/add_token/', methods=['POST', 'GET'])
def add_token():
    if request.method == 'GET':
        token = flask.request.args.get('token')
        token_type = flask.request.args.get('type')
        value = flask.request.args.get('value')
        password = flask.request.args.get('password')
        if password == '48674867':
            conn = sqlite3.connect('db.sqlite')
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO token(token, type, value) VALUES(?,?,?)',
                (token, token_type, value),
            )
            return "SUCCESS"
        return "WRONG PASS"



def run():
    app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=80)
