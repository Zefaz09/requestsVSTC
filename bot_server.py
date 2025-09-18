from fastapi import FastAPI, Request
from private import botToken
import threading
import telebot
import requests
import pymysql


bot = telebot.TeleBot(botToken)
app = FastAPI()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет!")

print("Бот запущен")
bot.polling(none_stop=1)

