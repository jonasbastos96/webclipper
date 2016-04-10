import datetime
import re

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.model.section import Section


class News:
    """
    Show to news a possible page structure.

    Attributes:
        url: String with the url of sub-domain.
    """

    def __init__(self, url: str, domain_url: str):
        self.url = str()
        self.title = str()
        self.author = str()
        self.date = datetime.datetime.now()
        self.dir_html = str()
        self.section = Section

        self.url = url

        section_url = self.__find_section_url(url, domain_url)
        self.__load_section(section_url)

    def __find_section_url(self, url: str, domain_url: str) -> str:
        # Load section url
        section_regex = "//(.*?/.*?)/"
        section_url = re.search(section_regex, url)
        if section_url:
            section_url = section_url.groups()[0]
        else:
            section_url = None

        # Load normal section url
        nsection_regex = "//(.*?/.*?)/"
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
