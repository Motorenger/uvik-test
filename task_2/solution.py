import sys
from contextlib import contextmanager
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ToDo


def connect_to_db():
    # return engine instance

    URL_PATH = "sqlite:///db.sqlite3"
    engine = create_engine(URL_PATH)

    return engine

# only for case of recreating database
# def create_table():
#     from models import Base
#     Base.metadata.create_all(connect_to_db())

#     print("Table created successfully")

# create_table()


@contextmanager
def db_session():
    # session context manager
    try:
        Session = sessionmaker(bind=connect_to_db())
        session = Session()

        yield session
    finally:
        session.close()


def welcome():
    # greeting

    print("Welcome!\n")


def todos_list():
    with db_session() as Session:
        todos_list = Session.query(ToDo).all()

        return [todo for todo in todos_list if not todo.done]


def create_todo():
    print("Creating todo)")

    todo = {}
    try:
        todo['title'] = input("Enter title:  ")
        todo['body'] = input("Enter body:  ")
    except ValueError():
        print("Invalid input")
        create_todo()

    todo_instance = ToDo(**todo)

    with db_session() as Session:

        Session.add(todo_instance)

        Session.commit()
        print("Successfully created todo")

    print("Create another one? (Yes - 1, Exit - press enter )")
    try:
        choice = int(input("Enter choice: "))
        if choice == 1:
            create_todo()
    except ValueError:
        pass


def delete_todo():
    try:
        choices = input("Enter todo number to delete"
                        "(divide with space if more than one): ").split(" ")
    except ValueError:
        print("Invalid input")
        delete_todo()

    with db_session() as Session:

        for choice in [int(x) for x in choices]:
            todo = todos_list()[choice-1]
            Session.delete(todo)

        Session.commit()
        print("Successfully deleted todos")


def mark_done():
    try:
        choices = input("Enter numbers of done todos:"
                        "(divide with space if more than one): ").split(" ")
    except ValueError:
        print("Invalid input")
        mark_done()

    with db_session() as Session:
        for choice in [int(x) for x in choices]:
            todo = todos_list()[choice-1]
            todo.done = True
            todo.done_date = date.today()
            Session.add(todo)
            Session.commit()
    print("Successfully marked as done")


def statistics():
    with db_session() as Session:
        todos_list = [todo for todo in
                      Session.query(ToDo).all() if todo.done_date]

    days = {}
    for todo in todos_list:

        if str(todo.done_date) not in days.keys():
            days[f"{todo.done_date}"] = 1
        else:
            days[f"{todo.done_date}"] += 1

    for day in days.items():
        print(f"{day[0]}: you've completed {day[1]} tasks!")


def main():

    welcome()

    while True:

        print("Your todos:\n")
        todos = todos_list()
        if todos:
            for i, todo in enumerate(todos):

                print(f"\t{i+1}. {todo.title}")
        else:
            print("No todos found(")

        print(
            "Options:\n"
            "\t1. Creare new todos\n"
            "\t2. Delete todos\n"
            "\t3. Mark as done\n"
            "\t4. Statistics\n"
            "\t5. EXIT\n"
        )

        try:
            choice = int(input("Enter yout choice:  "))
        except ValueError:
            print("Invalid enter")
            continue

        if choice == 1:
            create_todo()
        elif choice == 2:
            delete_todo()
        elif choice == 3:
            mark_done()
        elif choice == 4:
            statistics()
        elif choice == 4:
            sys.exit(0)


if __name__ == "__main__":
    main()
