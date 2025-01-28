from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from sqlalchemy.orm import Session
from database import get_session
from models import Student, Lesson, WeekDays, StudyGroup, Users

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
    student_profile = session.query(Student).join(StudyGroup, StudyGroup.id == Student.id_group).filter(Student.user_id == user_id).first()

    if student_profile:
        # Отправляем информацию о пользователе
        text = (
            f"Ваш профиль:\n"
            f"Имя: {student_profile.full_name}\n"
            f"Username: {student_profile.username}\n"
            f"ID: {student_profile.user_id}\n"
            f"Ширкоины: {student_profile.coins}\n"
            f"Группа: {student_profile.group.group_name}"  # Выводим название группы
        )
        await message.reply(text)
    else:
        # Если профиль не зарегистрирован, предлагаем зарегистрироваться
        await message.reply("Профиль не найден. Для регистрации используйте команду /register.")
    
    session.close()



# Клавиатура для выбора группы
def get_group_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    session = get_session()
    groups = session.query(StudyGroup).all()
    
    # Добавляем кнопку для каждой группы
    for group in groups:
        keyboard.add(KeyboardButton(group.group_name))
    
    # Кнопка для отмены
    keyboard.add(KeyboardButton("Отменить"))
    
    session.close()
    return keyboard

# Клавиатура для редактирования профиля
def get_profile_edit_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Изменить имя"))
    keyboard.add(KeyboardButton("Изменить тег"))
    keyboard.add(KeyboardButton("Изменить ширкоины"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard

async def create_user(message: types.Message):
    session = get_session()
    username = message.from_user.username
    if not username:
        await message.reply("У вас не установлен username. Пожалуйста, установите его в настройках Telegram.")
        return
    existing_profile = session.query(Users).filter_by(username = username).first()

    if existing_profile:
        await message.reply("Такой профиль уже есть :(")
    else:
        await message.answer("Введите пароль для вашего аккаунта:")

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
        
        # Запрос на выбор группы
        await message.reply("Пожалуйста, выберите вашу группу:", reply_markup=get_group_keyboard())

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

# Хендлер для выбора группы
async def process_group_selection(message: types.Message):
    session = get_session()
    user_id = message.from_user.id
    group_name = message.text

    # Проверяем, существует ли группа с таким названием
    group = session.query(StudyGroup).filter_by(group_name=group_name).first()

    if group:
        # Получаем профиль студента
        student_profile = session.query(Student).filter_by(user_id=user_id).first()
        if student_profile:
            # Обновляем группу у студента
            student_profile.id_group = group.id
            session.commit()
            await message.reply(f"Ваша группа успешно обновлена на: {group_name}")
        else:
            await message.reply("Не удалось найти ваш профиль.")
    else:
        await message.reply(f"Группа с названием '{group_name}' не найдена. Попробуйте выбрать другую группу.")
    
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

# Хендлер для команды /schedule
async def schedule_command(message: types.Message):
    user_id = message.from_user.id
    session = get_session()

    # Проверяем, зарегистрирован ли студент по user_id
    student = session.query(Student).filter(Student.user_id == user_id).first()

    if student:
        # Если студент зарегистрирован, используем его группу для получения расписания
        student_name = student.full_name  # Используем ФИО студента из его профиля

        # Получаем расписание для группы студента
        if not student.id_group:
            await message.reply(f"У студента {student_name} не указана группа. Пожалуйста, укажите группу в профиле.")
            return
        
        lessons = (
            session.query(Lesson, WeekDays)
            .join(WeekDays, Lesson.w_day == WeekDays.id)
            .filter(Lesson.group_id == student.id_group)  # Используем group_id для фильтрации
            .all()
        )

        if not lessons:
            await message.reply(f"Расписание для группы студента {student_name} не найдено.")
            return

        # Группировка уроков по дням недели
        days_of_week = {day.day_name: [] for day in session.query(WeekDays).all()}  # Словарь для хранения уроков по дням недели
        
        # Добавляем уроки в соответствующие дни недели
        for lesson, week_day in lessons:
            days_of_week[week_day.day_name].append(f"Время: {lesson.start_time} - {lesson.end_time}\nКабинет: {lesson.cabinet}")
        
        # Формируем расписание
        schedule_text = []
        for day_name, lessons_list in days_of_week.items():
            if lessons_list:  # Если есть уроки в этот день
                schedule_text.append(f"{day_name}:\n" + "\n".join(lessons_list))

        if schedule_text:
            await message.reply(f"Расписание для {student_name}:\n\n" + "\n\n".join(schedule_text))
        else:
            await message.reply(f"Для {student_name} не найдено уроков.")
    else:
        # Если студент не зарегистрирован, запрашиваем ФИО
        await message.reply("Пожалуйста, зарегистрируйтесь, указав ваше ФИО с помощью команды /register.")
    
    session.close()


async def admin_command(message: types.Message):
    await message.answer("Введите пароль для доступа к админ панели")

async def process_admin_password(message: types.Message):
    correct_password = "3721696"
    if message.text == correct_password:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        web_app_button = KeyboardButton(
            text="Open",
            web_app=WebAppInfo(url="vk.ru")
        )
        keyboard.add(web_app_button)
        await message.answer("Accsess")
    else:
        await message.answer("error")
