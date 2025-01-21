import telebot
import insert
from sqlalchemy import create_engine
import psycopg2

uName = "postgres"
pWord = "Dum_D4k"

engine = create_engine(f'postgresql+psycopg2://{uName}:{pWord}@localhost/SER_Tyuiu')
with engine.connect() as conn:

    BOT_TOKEN = "5702307330:AAF8x24G11wLONho88uHmsXzg0aYvdp0vzM"
    bot = telebot.TeleBot(BOT_TOKEN)
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, (
           """Что умеет этот бот?
                Добро пожаловать в бот Школы инженерного резерва! 
    
                Возможности бота:
                • ﻿﻿Получение расписания своего класса в выбранный день 
                • ﻿﻿Просмотр личного бюджета ширкоинов (для прошедших регистрацию)
                • ﻿﻿Просмотр перечня мероприятий шира
                • Просмотр личного профиля ученика (для пошедших регистрацию)
                • Предложить идею (здесь каждый может написать свои пожелания и идеи касаемо любой темы) (для прошедших регистрацию)
                • Сообщить об ошибке
    
                Советуем пройти регистрацию во вкладке «Профиль», чтобы открыть все возможности бота.
                Используйте команду /schedule <ФИО>, чтобы узнать расписание."""
        ))

    @bot.message_handler(commands=['schedule'])
    def schedule(message):
        try:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                bot.reply_to(message, "Пожалуйста, укажите ФИО студента после команды.\nПример: /schedule Иванов Иван Иванович")
                return

            student_name = args[1]

            schedule_data = insert.give_sch(conn, student_name)

            if not schedule_data:
                bot.reply_to(message, f"Расписание для {student_name} не найдено.")
            else:
                bot.reply_to(message, f"Расписание для {student_name}:\n\n{schedule_data}")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")



    print("Бот запущен...")
    bot.infinity_polling()
conn.close()