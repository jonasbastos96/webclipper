import datetime

from lxml import html

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.config import locations
from webclipper.model.domain import Domain
from webclipper.model.domain_elmundo import DomainElmundo
from webclipper.model.domain_globo import DomainGlobo
from webclipper.model.domain_uol import DomainUol
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

        if url:
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
        domain = Domain
        query = "SELECT * FROM domain " \
                "JOIN section " \
                "ON domain.url = section.domain_url " \
                "WHERE section.url = '{url}' " \
                "LIMIT 1;" \
            .format(url=self.url)
        result = dbconnection.select(query)

        # Load corretly domain
        for row in result:
            if row[1] == "Elmundo":
                domain = DomainElmundo()
            elif row[1] == "Uol":
                domain = DomainUol()
            elif row[1] == "Globo":
                domain = DomainGlobo()
            else:
                raise exceptions.UnsupportedDomain()

        if not domain:
            raise exceptions.UnsupportedSection()

        self.domain = domain

    # TODO add exceptions
    def generate_html(self, element: html.HtmlElement) -> str:
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
        filedir = locations.temp_dir + "news.html"
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

    def obtain_title(self, element: html.HtmlElement) -> str:
        titles = list()
        for structure in self.structures:
            try:
                title = structure.obtain_title(element)
                titles.append(title)
            except exceptions.TitleNotAvailable:
                continue

        if titles:
            return titles[0]
        else:
            raise exceptions.TitleNotAvailable()

    def obtain_author(self, element: html.HtmlElement) -> str:
        authors = list()
        for structure in self.structures:
            try:
                author = structure.obtain_author(element)
                authors.append(author)
            except exceptions.AuthorNotAvailable:
                continue

        if authors:
            return authors[0]
        else:
            raise exceptions.AuthorNotAvailable()

    def obtain_date(self, element: html.HtmlElement) -> datetime.datetime:
        dates = list()
        for structure in self.structures:
            try:
                date = structure.obtain_date(element)
                dates.append(date)
            except exceptions.DateNotAvailable:
                continue

        if dates:
            return dates[0]
        else:
            raise exceptions.DateNotAvailable()
