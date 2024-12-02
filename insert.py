from numpy import genfromtxt
from DB_ORM import *
from sqlalchemy.sql.expression import func
from datetime import time
from sqlalchemy import select
from sqlalchemy import insert

import datetime

with engine.connect() as conn:

    def Load_Data(file_name): # обработка файла после импорта. Сюда же можно завернуть и импорт самого файла
        data = genfromtxt(file_name, delimiter=';', dtype=None, skip_header=0, encoding="utf8")
        return data.tolist()

    def get_headrs(tbl): #Достаём заголовки стаблиц
        return list(conn.execute(select(tbl)).keys())


    def get_time_right(t):  #На случай пустой строки вместо времени
        if t == '':
            return '00:00'
        else:
            return t

    def getID(t_name): # Добывает идентификатор из выбранной таблицы
        stmt = select(func.max(t_name.id))
        answ = conn.execute(stmt)
        if answ == None:
            return 0
        for row in answ: #Нормально работает только так. Даже в гайде так указанно...
            return row[0]



    #def group_ins(data): # Легаси вставка на всякий
    #    sID = getID(Study_group)
    #    for i in data:
    #        sID += 1
    #        expr = (Study_group(id=sID, group_name=i))
    #        session.add(expr)
    #    session.commit()
    #    stmt = select(Study_group)
    #    print("voila")

    def create_expr(tbl, data): # создаём список данных, которые подлежат вставке. вход БЕЗ АЙДИШНИКА
        hdrs = get_headrs(tbl)
        res = []
        j = 1
        for row in data:
            lst = {}
            i = -1
            for hdr in hdrs:
                if hdr == "id": # присваиваем айдишник
                    i+=1
                    lst["id"] = getID(tbl) + (j)
                    continue
                elif hdr=="start_time" or hdr == "end_time": # Чиним пустые поля со временем
                    row[i] = get_time_right(row[i])
                lst[hdr] = row[i]
                i+=1
            j += 1
            res.append(lst)
        return res


    def insert_into(tbl, data): # Главная функция вставки
        expr = conn.execute(
            insert(tbl),
            create_expr(tbl, data)
            ,)
        conn.commit()


    #dat = [['Иванов Иван Иванович', '@3poIVA', 10], ["Петров Пётр Петрович", '@PetyaTretyi', 6]] #тест
    #datt = [[3,18], [4, 17]]
    #insert_into(Group_stud, datt)


    def give_sch(st_name): #Выдача расписания
        stmt = select(Lesson.start_time, Lesson.end_time, Lesson.cabinet, WeekDays.day_name).join(Lesson).join(Study_group).join(Group_stud).join(Student).where(Student.name == st_name)
        print(stmt)
        answ = conn.execute(stmt)
        for row in answ:
                print(f"{row[3]} \nВремя: С {str(row[0])[:-3]} до {str(row[1])[:-3]}  \nКабинет: {row[2]}")

    give_sch("Петров Пётр Петрович")

    #imp = Load_Data("schedule1.csv") #реализация вставки из файла в таблицу
    #for i in imp:
    #    print(i)
    #print(len(imp))


    conn.close()