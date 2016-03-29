import datetime


class search:
    def __init__(self):
        self.__id = int()
        self.__term = str()
        self.__status = int()
        self.__date_begin = datetime.datetime()
        self.__date_end = datetime.datetime()
        self.__limit_news = int()
        self.__domains = list()
        self.__news = list()
