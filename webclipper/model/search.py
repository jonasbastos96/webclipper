import datetime

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.model.domain_elmundo import DomainElmundo
from webclipper.model.domain_globo import DomainGlobo
from webclipper.model.domain_uol import DomainUol


class Search:
    def __init__(self, term: str, domains: list, date_begin: datetime.datetime,
                 date_end: datetime.datetime, limit_news: int = 0):
        self.id = int()
        self.term = str()
        self.status = int()
        self.date_begin = datetime.datetime.now()
        self.date_end = datetime.datetime.now()
        self.limit_news = int()
        self.domains = list()

        # Insering values
        self.term = term
        self.date_begin = date_begin
        self.date_end = date_end
        self.limit_news = limit_news

        # Load domains
        self.__load_domains(domains)

    def __load_domains(self, domains: list):
        if "Elmundo" in domains:
            domain = DomainElmundo()
            self.domains.append(domain)
        if "Uol" in domains:
            domain = DomainUol()
            self.domains.append(domain)
        if "Globo" in domains:
            domain = DomainGlobo()
            self.domains.append(domain)

        # if domains list is empty, raise an error
        if not self.domains:
            raise exceptions.UnexpectedBehavior()

    def news_in_database(self, url: str) -> int:
        query = "SELECT id FROM news " \
                "WHERE url = '{url}'" \
            .format(url=url)
        result = dbconnection.select(query)
        if result:
            return True
        else:
            return False

    def bind_news(self, url: str):
        # Retrieve id from news using url
        query = "SELECT id FROM news " \
                "WHERE url = '{url}'" \
            .format(url=url)
        result = dbconnection.select(query)
        try:
            news_id = result[0][0]
        except:
            raise exceptions.UnexpectedBehavior()

        # Check if news and search already is binded
        query = "SELECT * FROM search_has_news " \
                "WHERE search_id = {search_id} " \
                "AND news_id = {news_id}" \
            .format(search_id=self.id, news_id=news_id)
        result = dbconnection.select(query)
        if result:
            raise exceptions.InfoAlreadyBinded()

        # Record data in database
        query = "INSERT INTO search_has_news " \
                "VALUES ({search_id}, {news_id})" \
            .format(search_id=self.id, news_id=news_id)
        dbconnection.modify(query)

    def init_search(self):
        # Default values
        init_status = 1  # In progress
        date_begin = self.date_begin.strftime("%Y-%m-%d %H:%M:%S")
        date_end = self.date_end.strftime("%Y-%m-%d %H:%M:%S")

        # Insert into database
        query = "INSERT INTO search " \
                "(term, status, date_begin, date_end, limit_news) " \
                "VALUES ('{term}', {status}, '{date_begin}', '{date_end}', " \
                "{limit_news}); " \
            .format(term=self.term, status=init_status, date_begin=date_begin,
                    date_end=date_end, limit_news=self.limit_news)

        print(query)
        result = dbconnection.modify(query)

        # Retrieve last id
        if result:
            self.id = result
