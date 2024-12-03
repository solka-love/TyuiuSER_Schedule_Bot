from typing import List
from typing import Optional
#import sqlalchemy as salch
#import sqlalchemy.orm as salcho
from sqlalchemy import String, engine, ForeignKey, create_engine
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import time

import psycopg2

uName = "postgres"
pWord = "Dum_D4k"

engine = create_engine(f'postgresql+psycopg2://{uName}:{pWord}@localhost/SER_Tyuiu')

#Session = sessionmaker(bind=engine)
#session = Session()



#conn_string = "host='localhost' dbname='SER_Tyuiu'user='postgres' password='Dum_D4k'"

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
    start_time: Mapped[time]
    end_time: Mapped[time]
    w_day: Mapped[int] = mapped_column(ForeignKey("w_days.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("s_group.id"))
    #group_id: Mapped[List["s_group"]] = relationship(back_populates="id",cascade = "all, delete-orphan")

class Study_group(Base):
    __tablename__ = "s_group"

    id: Mapped[int] = mapped_column(primary_key=True)

    group_name: Mapped[str] = mapped_column(String[10])

class Group_stud(Base):
    __tablename__ = "group_stud"
    gr_id: Mapped[int] = mapped_column(ForeignKey(Study_group.id), primary_key=True)
    stud_id: Mapped[int] = mapped_column(ForeignKey(Student.id))

    def __repr__(self):
        return "<Node(nid='%s', title='%s')>" % (self.gr_id, self.stud_id)

class WeekDays(Base):
    __tablename__ = "w_days"
    id: Mapped[int] = mapped_column(primary_key=True)
    day_name: Mapped[str] = mapped_column(String(15))



