from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import insert 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
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
    )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        await update.message.reply_text(
            "Пожалуйста, укажите ФИО студента после команды.\n"
            "Например: /schedule Иванов Иван Иванович"
        )
        return

    student_name = " ".join(context.args)  
    try:
        print(f"Ищем расписание для {student_name}...")
        schedule = insert.give_sch(student_name)  
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")
        return

    if not schedule:
        await update.message.reply_text(f"Расписание для {student_name} не найдено.")
    else:
        await update.message.reply_text(f"Расписание для {student_name}:\n\n{schedule}")

if __name__ == "main":
    app = ApplicationBuilder().token("5702307330:AAF8x24G11wLONho88uHmsXzg0aYvdp0vzM").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", schedule))

    print("Бот запущен...")
    app.run_polling()