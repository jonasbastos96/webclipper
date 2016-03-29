import datetime


class Search:
    def __init__(self):
        self.id = int()
        self.term = str()
        self.status = int()
        self.dateBegin = datetime.datetime()
        self.dateEnd = datetime.datetime()
        self.limitNews = int()
        self.domains = list()
        self.news = list()
