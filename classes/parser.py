import asyncio
import requests

from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

from .models import Entry


class Parser(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    def get_html(self, url=None) -> str:
        url = self.url if url is None else url
        response = requests.get(url, headers=self.headers)
        return response.text

    def get_soup(self, url=None) -> BeautifulSoup:
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @abstractmethod
    def run(self) -> list[dict]:
        pass

    @abstractmethod
    def get_records(self) -> list:
        pass

    @abstractmethod
    async def parse(self, records: list) -> list[Entry]:
        pass

