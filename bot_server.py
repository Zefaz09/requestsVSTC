from private import botToken
import telebot
from telebot import types
import pymysql
from private import connection, cursor

bot = telebot.TeleBot(botToken)


keyboard = types.InlineKeyboardMarkup(row_width = 1)
kb = types.InlineKeyboardButton
keyboard.add(kb(text="Для студентов", callback_data="students"), kb(text="Для преподавателей", callback_data="teachers"))



@bot.message_handler(commands=['start'])
def start(message):
    # menu = bot.send_message(message.chat.id, "Добро пожаловать в бота для удобного просмотра рассписания УО\"ВГТК\"", reply_markup=keyboard)
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", [message.chat.id])
    username = cursor.fetchone()
    if not username:
        cursor.execute("INSERT INTO users (chat_id, username) VALUES (%s, %s)", [message.chat.id, message.from_user.username])
        connection.commit()
    else:
        bot.send_message(message.chat.id, f"Привет {username['username']}")
        



# @bot.callback_query_handler(func=lambda call: 1)
# def callback_inline(call):
#     if call.message:
#         bot.answer_callback_query(call.id)
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton("Студенты", callback_data="students"))
#         markup.add(types.InlineKeyboardButton("Преподаватели", callback_data="teachers"))

#         if call.data == "students":
#             bot.edit_message_text("Рассписание для студентов", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
#         elif call.data == "teachers":
#             bot.edit_message_text("Рассписание для преподавателей", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



print("Бот запущен")
bot.polling(none_stop=1)

