import os

import gspread
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_BOT_KEY')
bot = TeleBot(TOKEN)

candidates = {}

gc = gspread.service_account(filename='trans-century-436516-n6-fdde641b68dc.json')
sh = gc.open("Кандидаты").sheet1


@bot.message_handler(commands=['start', ])
def start(message):
    bot.send_message(message.from_user.id, "Привет. Ответь на вопросы бота и заполни информацию о себе")

    if message.chat.id not in candidates.keys():
        candidates[message.chat.id] = {}

    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton("Поехали!", callback_data='go')
    markup.add(item)

    bot.send_message(message.chat.id, "Нажми на кнопку 'Поехали!' для начала", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_start(call):
    try:
        if call.message:
            if call.data == 'go':
                bot.send_message(call.message.chat.id, 'ФИО:')
                bot.register_next_step_handler(call.message, ask_phone)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=call.message.text, reply_markup=None)

    except Exception as e:
        print(repr(e))


def ask_phone(message):
    candidates[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, 'Введи свой номер телефона:')
    bot.register_next_step_handler(message, ask_city)


def ask_city(message):
    candidates[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, 'В каком городе живешь?')
    bot.register_next_step_handler(message, ask_does_work)


def ask_does_work(message):
    candidates[message.chat.id]['city'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_1 = types.KeyboardButton("Работаю")
    item_2 = types.KeyboardButton("Учусь")
    item_3 = types.KeyboardButton("Нет")
    markup.add(item_1, item_2, item_3)

    bot.send_message(message.chat.id, 'В данный момент учишься или работаешь где-то?',
                     reply_markup=markup)
    bot.register_next_step_handler(message, ask_course)


def ask_course(message):
    candidates[message.chat.id]['does_work'] = message.text
    if message.text == 'Учусь':
        bot.send_message(message.chat.id, 'На каком курсе учишься?')
        bot.register_next_step_handler(message, ask_full_time)
    else:
        ask_full_time(message)


def ask_full_time(message):
    if message.text == 'Работаю' or message.text == 'Нет':
        candidates[message.chat.id]['course'] = '-'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_1 = types.KeyboardButton("Да")
    item_2 = types.KeyboardButton("Нет")
    markup.add(item_1, item_2)

    bot.send_message(message.chat.id, 'Можешь работать 5/2?', reply_markup=markup)
    bot.register_next_step_handler(message, ask_prog_lang)


def ask_prog_lang(message):
    candidates[message.chat.id]['full_time'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_1 = types.KeyboardButton("Да")
    item_2 = types.KeyboardButton("Нет")
    markup.add(item_1, item_2)

    bot.send_message(message.chat.id, 'Знаешь ли ты какой-то язык программирования на базовом уровне?',
                     reply_markup=markup)

    bot.register_next_step_handler(message, end_survey)


def end_survey(message):
    candidates[message.chat.id]['prog_lang'] = message.text
    bot.send_message(message.chat.id,
                     'Для отбора на вакансию необходимо пройти тест по ссылке\n '
                     'http://form-timer.com/start/aa88663a'
                     '\nНа тест дается 30 минут, необходимо набрать 25 баллов и более для дальнейшего взаимодействия')
    bot.send_message(message.chat.id,
                     f'Твоя информация:\nИмя: {candidates[message.chat.id]['name']}'
                     f'\nНомер телефона: {candidates[message.chat.id]['phone']}'
                     f'\nГород: {candidates[message.chat.id]['city']}'
                     f'\nРаботаешь/учишься: {candidates[message.chat.id]['does_work']}'
                     f'\nНа каком курсе: {candidates[message.chat.id]['course']}'
                     f'\nПолная занятость (5/2): {candidates[message.chat.id]['full_time']}'
                     f'\nЗнаешь ли язык программирования: {candidates[message.chat.id]['prog_lang']}'
                     )

    sh.append_row(
        [message.chat.id, candidates[message.chat.id]['name'], candidates[message.chat.id]['phone'],
         candidates[message.chat.id]['city'], candidates[message.chat.id]['does_work'],
         candidates[message.chat.id]['course'], candidates[message.chat.id]['full_time'],
         candidates[message.chat.id]['prog_lang']])

    del candidates[message.chat.id]


bot.polling(non_stop=True, interval=0)
