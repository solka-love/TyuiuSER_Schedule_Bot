import telebot
import insert


BOT_TOKEN = "5702307330:AAF8x24G11wLONho88uHmsXzg0aYvdp0vzM"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Приветственное сообщение."""
    bot.reply_to(message, (
        "Привет! Я бот для получения расписания.\n"
        "Используйте команду /schedule <ФИО>, чтобы узнать расписание.\n"
        "Пример: /schedule Иванов Иван Иванович"
    ))

@bot.message_handler(commands=['schedule'])
def schedule(message):
    """Обработка команды получения расписания."""
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "Пожалуйста, укажите ФИО студента после команды.\nПример: /schedule Иванов Иван Иванович")
            return

        student_name = args[1]

        schedule_data = insert.give_sch(student_name)

        if not schedule_data:
            bot.reply_to(message, f"Расписание для {student_name} не найдено.")
        else:
            bot.reply_to(message, f"Расписание для {student_name}:\n\n{schedule_data}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")



print("Бот запущен...")
bot.infinity_polling()