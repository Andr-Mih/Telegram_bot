from cmath import rect
import telebot
from time import sleep
from telebot import types
from config import token, data_base
import os
import sqlite3
import random
import utils


def record_bd():
    db = sqlite3.connect(data_base)
    curs = db.cursor()
    rownum = len(curs.execute('SELECT file_id FROM Music').fetchall())
    row = random.randint(1, rownum)
    record = curs.execute('SELECT * FROM Music WHERE id = ? ', (row,)).fetchall()
    db.close()
    return record



bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['test'])
def find_file_ids(message):
    for file in os.listdir('files/'):
        if file.split('.')[-1] == 'mp3':
            f = open('files/'+file, 'rb')
            msg = bot.send_audio(message.chat.id, f, None)
            bot.send_message(message.chat.id, msg.audio.file_id, reply_to_message_id=msg.message_id)
            sleep(3)

record = record_bd()
@bot.message_handler(commands = ['game'])
def game(message):
    markup = utils.generate_keyboard(record[0][2], record[0][3])
    bot.send_audio(message.chat.id, record[0][1], reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def check_answer(message):
    global record
    answer = record[0][2]
    print(answer, message.text)
    if message.text == answer:
        bot.send_message(message.chat.id, 'Right', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, 'Enter command /game')
    else:
        bot.send_message(message.chat.id, 'False', reply_markup=types.ReplyKeyboardMarkup())
        record = record_bd()
        game(message)



if __name__ == '__main__':
    
    bot.polling()