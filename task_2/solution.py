import sys
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, ToDo


def connect_to_db():
    # return engine instance

    URL_PATH = "sqlite:///db.sqlite3"
    engine = create_engine(URL_PATH)

    return engine

# only for case of recreating database
# def create_table():

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

        return todos_list


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
    pass


def main():

    welcome()

    while True:

        print("Your todos:\n")
        todos = todos_list()
        if todos:
            for i, todo in enumerate(todos):
                print(f"\t{i+1}. {todo.title},  Done-{todo.done}")
        else:
            print("No todos found(")

        print(
            "Options:\n"
            "\t1. Creare new todos\n"
            "\t2. Delete todos\n"
            "\t3. EXIT\n"
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
            sys.exit(0)


if __name__ == "__main__":
    main()
