import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import start_command, schedule_command, profile_command, register_command, edit_profile_command, process_edit_name, process_edit_tag, process_edit_coins

# Устанавливаем event loop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)

# Создаем экземпляры Bot и Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем хендлеры через Router
router = Router()

# Регистрируем команды с использованием фильтра Command
router.message.register(start_command, Command("start"))
router.message.register(schedule_command, Command("schedule"))
router.message.register(profile_command, Command("profile"))
router.message.register(register_command, Command("register"))

router.message.register(edit_profile_command, Command("edit"))
router.message.register(process_edit_name)
router.message.register(process_edit_tag)
router.message.register(process_edit_coins)

# Подключаем Router к Dispatcher
dp.include_router(router)

# Функция запуска бота
async def on_start():
    logging.info("Бот запущен...")
    # Запускаем цикл обработки сообщений
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем программу
    asyncio.run(on_start())
