from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column
from datetime import time
from hash import check_password, generate_password_hash

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
    id_group: Mapped[int] = mapped_column(ForeignKey("s_group.id"), nullable=True)

    # Связь с группой (через промежуточную таблицу)
    group = relationship("StudyGroup", back_populates="students", uselist=False)  # Отношение к одной группе

    def __repr__(self):
        return f"<Student(user_id={self.user_id}, username={self.username}, full_name={self.full_name})>"

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
    start_time: Mapped[time]  # Используем SQLAlchemy Time для работы с временем
    end_time: Mapped[time]    # Используем SQLAlchemy Time для работы с временем
    w_day: Mapped[int] = mapped_column(ForeignKey("w_days.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("s_group.id"))

    # Связь с группой
    group = relationship("StudyGroup", back_populates="lessons")

    # Связь с днями недели
    week_day = relationship("WeekDays", back_populates="lessons")

# Модель учебной группы
class StudyGroup(Base):
    __tablename__ = "s_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(20))

    # Связь с занятиями
    lessons = relationship("Lesson", back_populates="group")

    # Связь с группой студентов
    students = relationship("Student", back_populates="group")  # Отношение к студентам

# Модель дней недели
class WeekDays(Base):
    __tablename__ = "w_days"

    id: Mapped[int] = mapped_column(primary_key=True)
    day_name: Mapped[str] = mapped_column(String(15))

    # Связь с занятиями
    lessons = relationship("Lesson", back_populates="week_day")


class Users(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(128))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    
    role = relationship("Role", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)

class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    user = relationship("User", back_populates="role")
