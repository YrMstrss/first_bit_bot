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


bot.polling(non_stop=True, interval=0)
