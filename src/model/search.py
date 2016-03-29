import datetime


class search:
    def __init__(self):
        self.id = int()
        self.term = str()
        self.status = int()
        self.date_begin = datetime.datetime()
        self.date_end = datetime.datetime()
        self.limit_news = int()
        self.domains = list()
        self.news = list()
