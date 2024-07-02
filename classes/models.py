import datetime
from sqlmodel import Field, SQLModel


class Entry(SQLModel):
    id: int = Field(default=None, primary_key=True)
    date: datetime.date
    author_link: str
    author_name: str
    tags: str
    description: str


class Post(Entry, table=True):
    pass


class News(Entry, table=True):
    reading_time: str
    title: str
    link: str


class Article(Entry, table=True):
    reading_time: str
    title: str
    link: str
