from random import shuffle
from telebot import types

def generate_keyboard(right_answer, wrong):
    marup = types.ReplyKeyboardMarkup()
    all_answer = right_answer+','+wrong
    list_answer = []
    for item in all_answer.split(','):
        list_answer.append(item)
    shuffle(list_answer)
    for item in list_answer:
        marup.add(item)
    return marup