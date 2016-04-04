import sqlite3
from webclipper.model.structure import Structure
from webclipper.databases import dbinfo


class Section:
    """
    Show to news the possible pages' structures.

    Attributes:
        url: String with the url of sub-domain.
        structures: List of Pages.
    """

    def __init__(self, url=str()):
        # Define attributes
        self.url = url
        self.structures = list()

        # Load pages from database
        self.load_structures()

    def load_structures(self):
        """ Create and load pages objects from database """
        # Retrieve structures from database
        connection = sqlite3.connect(dbinfo.location)
        query = "SELECT * FROM structure " \
                "JOIN section " \
                "ON section.url = structure.section_url " \
                "WHERE section.url LIKE '%" + self.url + "%';"
        cursor = connection.execute(query)
        connection.close()

        # Instance and append each structure to list
        for row in cursor:
            structure = Structure(row=row)
            self.structures.append(structure)
