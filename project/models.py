from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Time

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    student_tag: Mapped[str] = mapped_column(String(32))
    coins: Mapped[int]

class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    cabinet: Mapped[str] = mapped_column(String(30))
    start_time: Mapped[Time]
    end_time: Mapped[Time]
    w_day: Mapped[int] = mapped_column(ForeignKey("w_days.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("s_group.id"))

class StudyGroup(Base):
    __tablename__ = "s_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(10))

class WeekDays(Base):
    __tablename__ = "w_days"

    id: Mapped[int] = mapped_column(primary_key=True)
    day_name: Mapped[str] = mapped_column(String(15))
