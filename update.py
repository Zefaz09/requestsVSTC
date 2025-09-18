import requests
from private import connection, cursor
import time
import zlib
from bot_server import bot

def checkUpdates(): 
    try:
        while True: 
            response = requests.get("http://127.0.0.1:1111")
            if response.status_code == 200:
                print("Подключено")

                # Получаем текущие данные страницы
                pageData = zlib.compress(response.text.encode('utf-8'))

                # Получаем сохранённые данные из базы
                cursor.execute("SELECT schedule FROM PageData")
                result = cursor.fetchone()  # fetchone вместо fetchall

                if result is None:
                    print("Получены первые данные")
                    cursor.execute("INSERT INTO PageData (schedule) VALUES (%s)", [pageData])
                    connection.commit()
                elif result['schedule'] != pageData:
                    print("Страница была обновлена")
                    cursor.execute("UPDATE PageData SET schedule = %s", [pageData])
                    connection.commit()
                    bot.send_message(1403014977, "Страница обновлена")
                else:
                    print("Страница не была обновлена")

            time.sleep(2)
    except Exception as e:
        import traceback
        print("Can`t get data:")
        traceback.print_exc()

checkUpdates()
