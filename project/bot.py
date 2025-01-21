import logging
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import start_command, schedule_command

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(start_command, commands=["start"])
dp.register_message_handler(schedule_command, commands=["schedule"])

if __name__ == "__main__":
    logging.info("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
