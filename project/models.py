from datetime import time
from sqlalchemy import String, Integer, ForeignKey, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column

# Базовый класс
class Base(DeclarativeBase):
    pass

# Модель студента
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # ID пользователя в Telegram
    username = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False)
    student_tag = Column(String(32))
    coins = Column(Integer, default=0)

    # Связь с занятиями (если вам нужно будет получить занятия для студента)
    lessons = relationship("Lesson", back_populates="student")
    groups = relationship("StudyGroup", secondary="student_group", back_populates="students")

    def __repr__(self):
        return f"<Student(user_id={self.user_id}, username={self.username}, full_name={self.full_name})>"

    # Метод для обновления информации о студенте
    def update_profile(self, full_name=None, student_tag=None, coins=None):
        if full_name:
            self.full_name = full_name
        if student_tag:
            self.student_tag = student_tag
        if coins is not None:
            self.coins = coins

# Модель занятия
class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    cabinet: Mapped[str] = mapped_column(String(30))
    start_time: Mapped[time]  # Используем time из стандартной библиотеки Python
    end_time: Mapped[time]    # Используем time из стандартной библиотеки Python
    w_day: Mapped[int] = mapped_column(ForeignKey("w_days.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("s_group.id"))

    # Связь с учебной группой (StudyGroup)
    group = relationship("StudyGroup", back_populates="lessons")

    # Связь с днями недели (WeekDays)
    week_day = relationship("WeekDays", back_populates="lessons")
    student = relationship("Student", back_populates="lessons")

# Модель учебной группы
class StudyGroup(Base):
    __tablename__ = "s_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(10))

    # Связь с занятиями
    lessons = relationship("Lesson", back_populates="group")

    # Связь с группой студентов
    students = relationship("Student", secondary="student_group", back_populates="groups") 

# Модель студентов в группе
class GroupStudents(Base):
    __tablename__ = "student_group"

    id_group: Mapped[int] = mapped_column(ForeignKey("s_group.id"))
    id_student: Mapped[int] = mapped_column(ForeignKey("student.id"))

    student = relationship("Student", back_populates="groups")
    group = relationship("StudyGroup", back_populates="students")

# Модель дней недели
class WeekDays(Base):
    __tablename__ = "w_days"

    id: Mapped[int] = mapped_column(primary_key=True)
    day_name: Mapped[str] = mapped_column(String(15))

    # Связь с занятиями
    lessons = relationship("Lesson", back_populates="week_day")
