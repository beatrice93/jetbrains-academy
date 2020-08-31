from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today().date()

# Menu:
choice = 1
while int(choice) != 0:
    print("")
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    choice = input()

    if int(choice) == 1:
        print("\nToday " + today.strftime('%#d %b') + ":")
        if session.query(Table).filter(Table.deadline == today).all() == []:
            print("Nothing to do!")
        else:
            task_counter = 1
            for row in session.query(Table).filter(Table.deadline == today).all():
                print("{}. {}".format(task_counter, row.task))
                task_counter += 1


    elif int(choice) == 2:
        for i in range(7):
            current_day = today + timedelta(days = i)
            print('\n' + current_day.strftime('%A %#d %b') + ':')
            if session.query(Table).filter(Table.deadline == current_day).all() == []:
                print("Nothing to do!")
            else:
                task_counter = 1
                for row in session.query(Table).filter(Table.deadline == current_day).all():
                    print("{}. {}".format(task_counter, row.task))
                    task_counter += 1

    elif int(choice) == 3:
        print("\nAll tasks:")
        if session.query(Table).all() == []:
            print("Nothing to do!")
        else:
            task_counter = 1
            for row in session.query(Table).order_by(Table.deadline).all():
                print("{}. {}. {}".format(task_counter, row.task, row.deadline.strftime('%#d %b')))
                task_counter += 1

    elif int(choice) == 4:
        print("\nMissed tasks:")
        if session.query(Table).filter(Table.deadline < today).all() == []:
            print("Nothing is missed!")
        else:
            task_counter = 1
            for row in session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all():
                print("{}. {}. {}".format(task_counter, row.task, row.deadline.strftime('%#d %b')))
                task_counter += 1


    elif int(choice) == 5:
        print("\nEnter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        new_row = Table(task = task, deadline = datetime.strptime(deadline, "%Y-%m-%d"))
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    elif int(choice) == 6:
        if session.query(Table).all() == []:
            print("Nothing to delete!")
        else:
            print("\nChoose the number of the task you want to delete:")
            task_counter = 1
            rows = session.query(Table).order_by(Table.deadline).all()
            for row in rows:
                print("{}. {}. {}".format(task_counter, row.task, row.deadline.strftime('%#d %b')))
                task_counter += 1
            row_to_delete = rows[int(input()) - 1]
            session.delete(row_to_delete)
            session.commit()




print("Bye!")
