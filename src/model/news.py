from .subdomain import Subdomain
from .domain import Domain
import datetime


class News:
    """ Show to news the possible pages' structures.

        Attributes:
            __url: String with the url of sub-domain.
    """

    def __init__(self):
        self.__url = str()
        self.__title = str()
        self.__author = str()
        self.__date = datetime.datetime()
        self.__dirHtml = str()
        self.__subdomain = Subdomain()
        self.__domain = Domain()
