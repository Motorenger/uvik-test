
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(Text)
    done = Column(Boolean)
    done_date = Column(Date)
