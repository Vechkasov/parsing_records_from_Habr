import datetime

from abc import ABC, abstractmethod
from sqlmodel import create_engine, Session, SQLModel

from classes.models import Entry


class IRepository(ABC):
    @abstractmethod
    def add(self, entry: Entry):
        pass


class CsvRepository(IRepository):
    def __init__(self, file_path: str = None):
        if file_path is None:
            now = datetime.date.today()
            file_path = f'data/{now.strftime("%d-%m-%Y")}.csv'
        self._file_path = file_path

    def add(self, entry: Entry):
        with open(self._file_path, 'a', encoding='utf-8') as file:
            file.write(f'{entry.date},{entry.__tablename__},{entry.author_link},{entry.author_name},{entry.tags}\n')


class SqlRepository(IRepository):
    def __init__(self, db_string: str = 'sqlite:///data.db'):
        self.engine = create_engine(db_string)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add(self, entry: Entry):
        self.session.add(entry)
        self.session.commit()
