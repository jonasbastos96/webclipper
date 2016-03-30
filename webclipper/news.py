from .subdomain import Subdomain
from .domain import Domain
import datetime


class News:
    """ Show to news the possible pages' structures.

        Attributes:
            url: String with the url of sub-domain.
    """

    def __init__(self):
        self.url = str()
        self.title = str()
        self.author = str()
        self.date = datetime.datetime()
        self.dirHtml = str()
        self.subdomain = Subdomain()
        self.domain = Domain()
