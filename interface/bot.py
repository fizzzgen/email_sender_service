# -*- coding: utf-8 -*-

import logging
import telebot
from engine import email_processor


TOKEN = '804994694:AAHPzpZMvWVMbjaIrkofTKh3PXbO4gFmkhQ'
HELLO_TEXT = 'Привет!'
HELP_TEXT = '''
    -ПОМОЩЬ-

    СКОНФИГУРИРУЙТЕ GOOGLE SPREADSHEET:

    в первом столбце - адрес получателя
    во втором столбце - текст сообщения в формате HTML
    в третьем столбце - тема письма
    в четвертоом столбце - ссылка на отписку от рассылки

    Не забудьте сделать таблицу публичной

    ЗАПУСТИТЕ РАССЫЛКУ, ОТПРАВИВ БОТУ СООБЩЕНИЕ:

    в первой строке сообщения должен быть ваш токен
    во второй - ваша почта
    в третьей - пароль от вашей почты
    в четвертой - сервер SMTP рассылки
    в пятой - ссылка на вашу google spreadsheet

'''
WRONG_CONFIG = 'Неправильный конфиг'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, HELLO_TEXT)
    bot.send_message(message.chat.id, HELP_TEXT)


@bot.message_handler()
def set_config(message):
    lines = message.text.split('\n')
    try:
        token = lines[0]
        login = lines[1]
        password = lines[2]
        server = lines[3]
        spreadsheet_link = lines[4]
        email_processor.schedule(
            token,
            login,
            password,
            server,
            spreadsheet_link
        )
    except Exception as ex:
        logging.exception(
            'Wrong config: {}'.format(message.text)
        )
        logging.exception(ex)
        bot.send_message(message.chat.id, WRONG_CONFIG)
        bot.send_message(message.chat.id, HELP_TEXT)


def poll():
    import threading
    tr = threading.Thread(
        target=bot.polling,
        kwargs={'none_stop': True},
    )
    tr.start()
    return tr
