from aiogram import types
from sqlalchemy.orm import Session
from database import get_session
from models import Student, Lesson, StudyGroup, WeekDays

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
            .filter(Student.name == student_name)
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
