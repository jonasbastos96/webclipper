from .page import Page


class Subdomain:
    """ Show to news the possible pages' structures.

        Attributes:
            url: String with the url of sub-domain.
            pages: List of Pages.
    """

    def __init__(self):
        # Define attributes
        self.url = str()
        self.pages = list()

        # Load pages from database
        self.loadPages()

    def loadPages(self):
        """ Create and load pages objects from database """
        return None
