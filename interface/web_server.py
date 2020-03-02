from flask import Flask
from engine import email_processor
from flask import request

app = Flask(__name__)


@app.route('/')
def ping():
    return 'Working...'


@app.route('/schedule/')
def schedule():
    if request.method == 'POST':
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
