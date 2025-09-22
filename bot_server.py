from private import botToken
import telebot
from telebot import types
import pymysql
from private import connection, cursor
from parse import getScheduleForStudents, getDate

bot = telebot.TeleBot(botToken)


keyboard = types.InlineKeyboardMarkup(row_width = 1)
kb = types.InlineKeyboardButton
keyboard.add(kb(text="Для студентов", callback_data="students"), kb(text="Для преподавателей", callback_data="teachers"))

markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton("Для студентов", callback_data="students"))
markup.add(types.InlineKeyboardButton("Для преподавателей", callback_data="teachers"))

studentsMarkup = types.InlineKeyboardMarkup(row_width=1)
studentsMarkup.add(kb(text="Сегодня", callback_data="today"), kb(text="Завтра", callback_data="tomorrow"), kb(text="Назад", callback_data="back"))


def viewSchedule(group):
    return "\n".join(getScheduleForStudents(group)[1])


@bot.message_handler(commands=['start'])
def start(message):
    # menu = bot.send_message(message.chat.id, "Добро пожаловать в бота для удобного просмотра рассписания УО\"ВГТК\"", reply_markup=keyboard)
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", [message.chat.id])
    username = cursor.fetchone()
    if not username:
        cursor.execute("INSERT INTO users (chat_id, username) VALUES (%s, %s)", [message.chat.id, message.from_user.username])
        connection.commit()
        bot.send_message(message.chat.id, f"Привет, {message.from_user.username}! Этот бот создан для удобного промотра рассписания с сайта УО\"ВГТК\". Какое рассписание тебя интересует?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f"Привет {username['username']}! Нажми на интересующее тебя рассписание ниже", reply_markup=keyboard)  


@bot.message_handler(content_types=['text'])
def messages(message):
    cursor.execute("SELECT stage FROM users WHERE chat_id = %s", [message.chat.id])
    stage = cursor.fetchone()
    if not stage:
        pass
    elif stage['stage'] == "getGroup":
        cursor.execute("INSERT INTO students (chat_id, groupName) VALUES (%s, %s)", [message.chat.id, message.text])
        connection.commit()
        cursor.execute("SELECT message_id FROM users WHERE chat_id = %s", [message.chat.id])
        message_id = cursor.fetchone()
        if message_id:
            bot.edit_message_text(viewSchedule(message.text), chat_id=message.chat.id, message_id=message_id['message_id'], reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)
       
    


@bot.callback_query_handler(func=lambda call: 1)
def callback_inline(call):
    if call.message:
        bot.answer_callback_query(call.id)
        
        if call.data == "students":
            cursor.execute("SELECT groupName FROM students WHERE chat_id = %s", [call.message.chat.id])
            group = cursor.fetchone()
            if not group:
                bot.edit_message_text("Пришли имя своей группы", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=studentsMarkup)
                cursor.execute("UPDATE users SET stage = 'getGroup', message_id = %s WHERE chat_id = %s", [call.message.message_id, call.message.chat.id])
                connection.commit()
            else:
                bot.edit_message_text(viewSchedule(group['groupName']), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=studentsMarkup)

                
                
        elif call.data == "teachers":
            bot.edit_message_text("Рассписание для преподавателей", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

        elif call.data == "back":
            cursor.execute("SELECT stage, message_id FROM users WHERE chat_id = %s", [call.message.chat.id])
            data = cursor.fetchone()
            if data:
                try:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=data['message_id'], reply_markup=markup)
                except telebot.apihelper.ApiTelegramException as e:
                    if "message is not modified" in str(e):
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=data['message_id'], reply_markup=markup)                    
                    else:
                        raise  

            
            
            
        


print("Бот запущен")
bot.polling(none_stop=1)

