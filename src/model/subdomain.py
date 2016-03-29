from .page import Page


class Subdomain:
    """ Show to news the possible pages' structures.

        Attributes:
            __url: String with the url of sub-domain.
            __pages: List of Pages.
    """

    def __init__(self):
        # Define attributes
        self.__url = str()
        self.__pages = list()

        # Load pages from database
        self.__load_pages()

    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_pages(self):
        return self.__pages

    def set_pages(self, pages):
        self.__pages = pages

    def add_page(self, page: Page()):
        """ Add page to list """
        self.__pages.append(page)

    def remove_page(self, page: Page()):
        """ Remove page of list """
        self.__pages.remove(page)

    def __load_pages(self):
        """ Create and load pages objects from database """
        return None
