import datetime
import re

from lxml import html

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.model.section import Section


class News:
    """
    Show to news a possible page structure.

    Attributes:
        url: String with the url of sub-domain.
    """

    def __init__(self, url: str, domain_url: str, date: datetime.datetime):
        self.url = url
        self.title = str()
        self.author = str()
        self.date = date
        self.dir_html = str()
        self.section = Section()
        self.element = html.HtmlElement()

        # Load section
        section_url = self.__find_section_url(url, domain_url)
        self.__load_section(section_url)

        # Load source and element
        self.element = self.section.domain.obtain_element(self.url)

        # Load informations about news
        self.__load_title()
        self.__load_author()

    def __find_section_url(self, url: str, domain_url: str) -> str:
        # Load section url
        section_regex = "//(.*?/.*?)/"
        section_url = re.search(section_regex, url)
        if section_url:
            section_url = section_url.groups()[0]
        else:
            section_url = None

        # Load normal section url
        nsection_regex = "//(.*?)/(.*?)/"
        nsection_url = re.search(nsection_regex, url)
        if nsection_url:
            nsection_url = nsection_url.groups()[0]
        else:
            nsection_url = None

        # Make query
        query = "SELECT url FROM section " \
                "WHERE url IN ("
        if section_url:
            query = query + "\"" + section_url + "\", "
        if nsection_url:
            query = query + "\"" + nsection_url + "\", "
        query = query + "\"" + domain_url + "\") "
        query += "ORDER BY importance DESC"

        result = dbconnection.select(query)

        if result:
            url = result[0][0]
        else:
            raise exceptions.UnsupportedURL()

        return url

    def __load_section(self, section_url: str):
        self.section = Section(section_url)

    def __load_title(self):
        try:
            self.title = self.section.obtain_title(self.element)
        except exceptions.TitleNotAvailable:
            self.title = None

    def __load_author(self):
        try:
            self.author = self.section.obtain_author(self.element)
        except exceptions.AuthorNotAvailable:
            self.author = None

    def __load_date(self):
        try:
            self.date = self.section.obtain_date(self.element)
        except exceptions.DateNotAvailable:
            self.date = None

    def retrieve_news(self):
        print(self.section.generate_html(self.element))
