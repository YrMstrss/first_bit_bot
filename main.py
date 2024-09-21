import os
import telebot
from dotenv import load_dotenv


env_path = '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
