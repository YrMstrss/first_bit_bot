import os
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_BOT_KEY')
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def start(message):
    bot.send_message(message.from_user.id, "Привет. Ответь на вопросы бота и заполни информацию о себе")

    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton("Поехали!", callback_data='go')
    markup.add(item)

    bot.send_message(message.chat.id, "Нажми на кнопку 'Поехали!' для начала", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_start(call):
    try:
        if call.message:
            bot.send_message(call.message.chat.id, 'Полное имя:')

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Нажми на кнопку 'Поехали!' для начала", reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(non_stop=True, interval=0)
