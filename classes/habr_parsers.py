import datetime
import logging
import time

from .parser import Parser
from bs4 import BeautifulSoup
from abc import abstractmethod


from .models import Post, Article, News, Entry


class CommonParseData:
    @staticmethod
    def get_description(record: BeautifulSoup) -> str:
        a = record.find_all('div', class_='article-formatted-body')
        return a[0].text

    @staticmethod
    def get_tags(record: BeautifulSoup) -> str:
        record_tags = (record.find('div', class_='tm-publication-hubs')
                       .find_all('span', class_='tm-publication-hub__link-container'))
        tags = []
        for tag in record_tags:
            spn = tag.find('span')
            tags.append(spn.text.strip())
        return '* '.join(tags)

    @staticmethod
    def get_date(record: BeautifulSoup, entry_type: str = None) -> str:
        date = (record.find('div', class_=f'tm-{entry_type}-snippet__meta')
        .find('a', class_='tm-article-datetime-published_link')
        .find_next()['title'])
        date = datetime.datetime.strptime(date[:10], '%Y-%m-%d').date()
        return date

    @staticmethod
    def get_author_info(record: BeautifulSoup, entry_type: str) -> (str, str):
        author_link = (record.find('div', class_=f'tm-{entry_type}-snippet__meta')
        .find('a', class_='tm-user-info__userpic')['href'])
        author_name = (record.find('div', class_=f'tm-{entry_type}-snippet__meta')
                       .find('a', class_='tm-user-info__username').text.strip())
        return author_name, author_link


class AdditionParseData(CommonParseData):
    @staticmethod
    def get_link(record: BeautifulSoup) -> str:
        return record.find('h2').find_next('a')['href']

    @staticmethod
    def get_reading_time(record: BeautifulSoup) -> str:
        return (record.find('div', class_='tm-article-snippet__stats')
                .find('span', class_='tm-article-reading-time__label').text)

    @staticmethod
    def get_title(record: BeautifulSoup) -> str:
        return record.find('h2').find_next('span').text


class HabrParser(Parser):
    def __init__(self, entry_type: str):
        url = 'https://habr.com/ru/flows'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36'
        }

        self.logger = logging.getLogger('logger')
        logging.basicConfig(filename='info.log', level=logging.INFO,
                            format='%(asctime)s - %(module)s - %(message)s')

        super().__init__(url, headers)

        self.groups_type = ['admin', 'develop']
        self.data = {'type': entry_type, 'entries': []}

    def get_records(self, url=None) -> list:
        soup = self.get_soup(url)
        return soup.find_all('article')

    def run(self) -> list[dict]:
        for group in self.groups_type:
            start = time.monotonic()
            url = self.url + '/' + group + '/' + self.data['type']
            records = self.get_records(url)
            data = self.parse(records)
            self.data['entries'].extend(data)
            self.logger.info(f'{group}/{self.data["type"]} - {len(data)} | {time.monotonic() - start}')
        return self.data

    @abstractmethod
    def parse(self, records: list) -> list[Entry]:
        pass


class HabrPosts(HabrParser, CommonParseData):
    def __init__(self):
        entry_type = 'posts'
        super().__init__(entry_type)

    def parse(self, records: list) -> list[Entry]:
        result = []
        for record in records:
            date = self.get_date(record, 'post')

            if date != datetime.date.today():
                continue

            tags = self.get_tags(record)
            author_name, author_link = self.get_author_info(record, 'post')
            description = self.get_description(record)
            result.append(Post(date=date, tags=tags, author_link=author_link,
                               author_name=author_name, description=description))
        return result


class HabrArticles(HabrParser, AdditionParseData):
    def __init__(self):
        entry_type = 'articles'
        super().__init__(entry_type)

    def parse(self, records: list) -> list[Entry]:
        result = []
        for record in records:
            date = self.get_date(record, 'article')

            if date != datetime.date.today():
                continue

            tags = self.get_tags(record)
            author_name, author_link = self.get_author_info(record, 'article')
            description = self.get_description(record)

            link = self.get_link(record)
            reading_time = self.get_reading_time(record)
            title = self.get_title(record)

            result.append(Article(date=date, tags=tags, author_link=author_link,
                                  author_name=author_name, description=description,
                                  reading_time=reading_time, title=title, link=link))
        return result


class HabrNews(HabrParser, AdditionParseData):
    def __init__(self):
        entry_type = 'news'
        super().__init__(entry_type)

    def parse(self, records: list) -> list[Entry]:
        result = []
        for record in records:
            date = self.get_date(record, 'article')

            if date != datetime.date.today():
                continue

            tags = self.get_tags(record)
            author_name, author_link = self.get_author_info(record, 'article')
            description = self.get_description(record)

            link = self.get_link(record)
            reading_time = self.get_reading_time(record)
            title = self.get_title(record)

            result.append(News(date=date, tags=tags, author_link=author_link,
                               author_name=author_name, description=description,
                               reading_time=reading_time, title=title, link=link))
        return result
