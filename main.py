from classes import Manager
from classes import HabrPosts, HabrArticles, HabrNews
from classes import SqlRepository, CsvRepository

m = Manager([HabrPosts(), HabrArticles(), HabrNews()], [SqlRepository(), CsvRepository()])
m.run()
