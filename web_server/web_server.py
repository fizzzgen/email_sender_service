from flask import Flask
from engine import email_processor
from flask import request
from flask import render_template

app = Flask(__name__, template_folder="static")


@app.route('/')
def ping():
    return render_template('form.html')


@app.route('/schedule/', methods=['POST'])
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
        return "Success!"
