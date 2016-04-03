from .section import Section
from .domain import Domain
import datetime


class News:
    """
    Show to news a possible page structure.

    Attributes:
        url: String with the url of sub-domain.
    """

    def __init__(self):
        self.url = str()
        self.title = str()
        self.author = str()
        self.date = datetime.datetime()
        self.dirHtml = str()
        self.section = Section()
        self.domain = Domain()
