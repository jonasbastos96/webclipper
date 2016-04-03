class Section:
    """
    Show to news the possible pages' structures.

    Attributes:
        url: String with the url of sub-domain.
        structures: List of Pages.
    """

    def __init__(self):
        # Define attributes
        self.url = str()
        self.structures = list()

        # Load pages from database
        self.load_pages()

    def load_pages(self):
        """ Create and load pages objects from database """
        return None
