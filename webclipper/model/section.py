from lxml import html

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.config import locations
from webclipper.model.domain import Domain
from webclipper.model.domain_elmundo import DomainElmundo
from webclipper.model.structure import Structure


class Section:
    """
    Show to news the possible pages' structures.

    Attributes:
        url: String with the url of sub-domain.
        structures: List of Pages.
    """

    # TODO add exception when instancing a unsupported url
    def __init__(self, url: str = None):
        # Define attributes
        self.url = url
        self.domain = Domain()
        self.structures = list()

        # Load pages from database
        self.load_structures()

        # Load domain
        self.load_domain()

    def load_structures(self):
        """ Create and load pages objects from database """
        # Retrieve structures from database
        query = "SELECT * FROM structure " \
                "JOIN section " \
                "ON section.url = structure.section_url " \
                "WHERE section.url = '" + self.url + "';"
        result = dbconnection.select(query)

        # Instance and append each structure to list
        for row in result:
            structure = Structure(row=row)
            self.structures.append(structure)

    def load_domain(self):
        # Retrieve structures from database
        domain = None
        query = "SELECT * FROM domain " \
                "JOIN section " \
                "ON domain.url = section.domain_url " \
                "WHERE section.url = '{url}' " \
                "LIMIT 1;" \
            .format(url=self.url)
        result = dbconnection.select(query)

        # Load corretly domain
        for row in result:
            if row[0] == "http://www.elmundo.es/":
                domain = DomainElmundo(row=row)
            else:
                domain = Domain(row=row)

        if not domain:
            raise exceptions.UnsupportedSection()

        self.domain = domain

    # TODO add exceptions
    def generate_html(self, url: str) -> str:
        # Obtain element from link
        element = self.domain.obtain_element(url)

        # Filter page
        self.filter_element(element)

        # Generate content
        contents = self.__generate_content(element)

        # Compare for the best content
        best_content = self.__analyse_content(contents)

        # Parse to HTML file
        output_file = self.__parse_to_html(best_content)

        return output_file

    def __generate_content(self, element: html.HtmlElement) -> list:
        contents = list()
        for structure in self.structures:
            try:
                content = structure.parse_to_content(element)
                contents.append(content)
            except exceptions.UnsupportedURL:
                pass
        return contents

    def filter_element(self, element: html.HtmlElement):
        return None

    def __analyse_content(self, contents: list) -> html.HtmlElement:
        max_parag = 0
        best_content = html.HtmlElement

        for content in contents:
            path = "//p"
            nodes = content.xpath(path)
            if len(nodes) > max_parag:
                max_parag = len(nodes)
                best_content = content

        return best_content

    def __parse_to_html(self, content: html.HtmlElement) -> str:
        # Set default domain encoding
        encoding = self.domain.encoding

        # Download pending images
        self.__resolve_images(content)

        # Transform content to html text source
        source = html.tostring(content, encoding=encoding).decode(encoding)

        # Create a HTML file
        filedir = locations.temp_folder + "news.html"
        file = open(filedir, "w", encoding=encoding)
        file.write(source)
        file.close()
        return filedir

    def __resolve_images(self, content: html.HtmlElement):
        # Select images from content
        path = "//img"
        images_node = content.xpath(path)

        # Try to download each image
        for images in images_node:
            image_url = images.get("orig_src")
            self.domain.download_image(image_url)
