from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.orm import Session
from database import get_session
from models import Student, Lesson, WeekDays, StudyGroup

# Хендлер для команды /start
async def start_command(message: types.Message):
    text = (
        "Добро пожаловать в бот Школы инженерного резерва! \n\n"
        "Возможности бота:\n"
        "- Получение расписания класса в выбранный день.\n"
        "- Просмотр личного бюджета ширкоинов.\n"
        "- Предложить идею или сообщить об ошибке.\n\n"
        "Для регистрации используйте команду /profile.\n"
        "Для расписания используйте /schedule <ФИО>."
    )
    await message.reply(text)

# Хендлер для команды /profile
async def profile_command(message: types.Message):
    session = get_session()
    user_id = message.from_user.id

    # Получаем профиль пользователя из базы данных
    student_profile = session.query(Student).filter_by(user_id=user_id).first()

    if student_profile:
        # Отправляем информацию о пользователе
        text = (
            f"Ваш профиль:\n"
            f"Имя: {student_profile.full_name}\n"
            f"Username: {student_profile.username}\n"
            f"ID: {student_profile.user_id}\n"
            f"Ширкоины: {student_profile.coins}"
        )
        # await message.reply(text, reply_markup=get_profile_edit_keyboard())
        await message.reply(text)
    else:
        # Если профиль не зарегистрирован, предлагаем зарегистрироваться
        await message.reply("Профиль не найден. Для регистрации используйте команду /register.")
    
    session.close()

# Клавиатура для редактирования профиля
def get_profile_edit_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Изменить имя"))
    keyboard.add(KeyboardButton("Изменить тег"))
    keyboard.add(KeyboardButton("Изменить ширкоины"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard

# Хендлер для команды /register (регистрация профиля)
async def register_command(message: types.Message):
    session = get_session()
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    # Проверяем, существует ли уже профиль
    existing_profile = session.query(Student).filter_by(user_id=user_id).first()

    if existing_profile:
        await message.reply("Ваш профиль уже зарегистрирован!")
    else:
        # Создаем новый профиль
        new_student = Student(
            user_id=user_id,
            username=username,
            full_name=full_name
        )
        session.add(new_student)
        session.commit()

        await message.reply(f"Ваш профиль успешно зарегистрирован!\nИмя: {full_name}\nUsername: {username}")
    
    session.close()

# Хендлер для редактирования профиля
async def edit_profile_command(message: types.Message):
    user_id = message.from_user.id
    session = get_session()
    
    profile = session.query(Student).filter_by(user_id=user_id).first()
    
    if profile:
        if message.text == "Изменить имя":
            await message.answer("Введите новое имя:")
            session.close()
            return
        elif message.text == "Изменить тег":
            await message.answer("Введите новый тег:")
            session.close()
            return
        elif message.text == "Изменить ширкоины":
            await message.answer("Введите новое количество ширкоинов:")
            session.close()
            return
        elif message.text == "Назад":
            await message.answer("Вы вернулись в меню профиля.", reply_markup=get_profile_edit_keyboard())
            session.close()
            return
    else:
        await message.answer("Профиль не найден. Для регистрации используйте команду /register.")
        session.close()

# Обработчик для изменения имени
async def process_edit_name(message: types.Message):
    new_name = message.text
    user_id = message.from_user.id
    session = get_session()

    profile = session.query(Student).filter_by(user_id=user_id).first()
    if profile:
        profile.full_name = new_name
        session.commit()
        await message.answer(f"Ваше имя успешно обновлено на: {new_name}", reply_markup=get_profile_edit_keyboard())
    session.close()

# Обработчик для изменения тега
async def process_edit_tag(message: types.Message):
    new_tag = message.text
    user_id = message.from_user.id
    session = get_session()

    profile = session.query(Student).filter_by(user_id=user_id).first()
    if profile:
        profile.student_tag = new_tag
        session.commit()
        await message.answer(f"Ваш тег успешно обновлен на: {new_tag}", reply_markup=get_profile_edit_keyboard())
    session.close()

# Обработчик для изменения ширкоинов
async def process_edit_coins(message: types.Message):
    try:
        new_coins = float(message.text)
        user_id = message.from_user.id
        session = get_session()

        profile = session.query(Student).filter_by(user_id=user_id).first()
        if profile:
            profile.coins = new_coins
            session.commit()
            await message.answer(f"Количество ширкоинов успешно обновлено на: {new_coins}", reply_markup=get_profile_edit_keyboard())
        session.close()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное количество ширкоинов.")

async def schedule_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Пожалуйста, укажите ФИО студента.\nПример: /schedule Иванов Иван Иванович")
        return

    student_name = args[1]
    session = get_session()
    try:
        lessons = (
            session.query(Lesson, WeekDays)
            .join(WeekDays, Lesson.w_day == WeekDays.id)
            .join(StudyGroup, Lesson.group_id == StudyGroup.id)
            .join(Student, Student.id == Lesson.group_id)
            .filter(Student.full_name == student_name)
            .all()
        )

        if not lessons:
            await message.reply(f"Расписание для {student_name} не найдено.")
            return

        schedule_text = "\n\n".join(
            f"{lesson[1].day_name}\nВремя: {lesson[0].start_time} - {lesson[0].end_time}\nКабинет: {lesson[0].cabinet}"
            for lesson in lessons
        )
        await message.reply(f"Расписание для {student_name}:\n\n{schedule_text}")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        session.close()