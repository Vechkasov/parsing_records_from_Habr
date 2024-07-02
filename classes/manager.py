import logging
import time

from .parser import Parser
from .repository import IRepository


class Manager:
    def __init__(self, parsers: list[Parser], repositories: IRepository):
        self.repository = repositories
        self.parsers = parsers
        self.logger = logging.getLogger('logger')

        logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(module)s - %(message)s')

    def run(self):
        info = []
        start = time.monotonic()
        for parser in self.parsers:
            data = parser.run()
            info.append(f'{data["type"]}: {len(data["entries"])}')
            for record in data['entries']:
                for rep in self.repository:
                    rep.add(record)
        self.logger.info(f'parsed: {" ".join(info)} in {time.monotonic() - start} \n\n')
