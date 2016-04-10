import datetime

from lxml import html

from webclipper import exceptions
from webclipper import utils
from webclipper.config import dbconnection


class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    # Class atributes

    # Instance attributes
    def __init__(self, **kwargs):
        self.id = int()
        self.title_tag = list()
        self.subheading_tag = list()
        self.text_tag = list()
        self.image_tag = list()
        self.caption_tag = list()
        self.title_path = str()
        self.author_path = str()
        self.date_path = str()
        self.content_path = str()
        self.date_format = str()

        if "row" in kwargs.keys():
            self.id = kwargs["row"][0]
            if kwargs["row"][1]:
                self.title_tag = kwargs["row"][1].split(",")
            if kwargs["row"][2]:
                self.subheading_tag = kwargs["row"][2].split(",")
            if kwargs["row"][3]:
                self.text_tag = kwargs["row"][3].split(",")
            if kwargs["row"][4]:
                self.image_tag = kwargs["row"][4].split(",")
            if kwargs["row"][5]:
                self.caption_tag = kwargs["row"][5].split(",")
            self.title_path = kwargs["row"][6]
            self.author_path = kwargs["row"][7]
            self.date_path = kwargs["row"][8]
            self.content_path = kwargs["row"][9]
            self.date_format = kwargs["row"][10]

    def parse_to_content(self, element: html.HtmlElement) -> html.HtmlElement:
        source = str()

        # Get valid content nodes
        nodes = element.xpath(self.content_path)

        # Format each according its pattern
        for node in nodes:
            try:
                if node.tag in self.subheading_tag:
                    source += self.__obtain_subheading(node)
                elif node.tag in self.text_tag:
                    source += self.__obtain_text(node)
                elif node.tag in self.image_tag:
                    source += self.__obtain_image(node)
                elif node.tag in self.caption_tag:
                    source += self.__obtain_caption(node)
            except exceptions.EmptyNodeContent:
                pass

        # Add base html to content
        source = self.__add_base_html(source)

        # Create a new html element with content
        content = html.fromstring(source)

        # Check if is a valid content
        if not self.__is_valid_content(content):
            raise exceptions.UnsupportedURL()

        return content

    def __add_base_html(self, source: str):
        # Query for correct encoding
        query = "SELECT domain.encoding from domain " \
                "JOIN section ON domain.url = section.domain_url " \
                "JOIN structure ON section.url = structure.section_url " \
                "WHERE structure.id = {id} " \
                "LIMIT 1" \
            .format(id=self.id)
        result = dbconnection.select(query)
        if result:
            encoding = result[0][0]
        else:
            raise exceptions.IncorrectQuery()

        # Build specific head for page
        head = "<head>\n" \
               "<style>\n" \
               ".main-content {{text-align: justify; text-indent: 50px;}}\n" \
               ".caption {{text-align: center;}}\n" \
               "img {{display: block; margin: 0 auto; width: 400px;}}\n" \
               "</style>\n" \
               "<meta charset='{encoding}'>\n" \
               "<head>\n" \
            .format(encoding=encoding)

        # Build specific body for page
        body_begin = "<body>\n"
        body_end = "</body>\n"

        # Merge head, body and source
        source = head + body_begin + source + body_end

        return source

    def __obtain_subheading(self, node: html.HtmlElement) -> str:
        # Check if node have content
        if not node.text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        text_formated = utils.remove_spaces(node.text)
        source = "<h2>" + text_formated + "</h2>\n"

        return source

    def __obtain_text(self, node: html.HtmlElement) -> str:
        # Prepare text to be analysed
        text = self.__disassembly_text(node, format_text=True)
        text = utils.remove_spaces(text)

        # Check if disassembled text have content
        if not text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        source = "<p class='main-content'>" + text + "</p>\n"

        return source

    def __disassembly_text(self, node: html.HtmlElement, is_first=True,
                           format_text=False) -> str:
        text = str()

        # Tags to ignore
        if node.tag in ("script",):
            return text

        # If format text is enabled:
        if format_text:
            # Check if node is a breakspace <br> or a text
            if node.tag == "br":
                text = "<br>"
            elif node.text:
                text += node.text

            # If text use tag strong, make it strong (bold)
            if node.tag == "strong":
                text = "<strong>" + text + "</strong>"
            # If text use em tag, make it em (italic)
            elif node.tag == "em":
                text = "<em>" + text + "</em>"
        elif node.text:
            text += node.text

        # Check if node have childrens and retrieve its texts
        childrens = node.xpath("./*")
        if childrens:
            for child in childrens:
                text += self.__disassembly_text(child, False)

        # If is a children, also check the tail
        if not is_first:
            if node.tail:
                text += node.tail

        return text

    def __obtain_image(self, node: html.HtmlElement) -> str:
        # Check if node have an image url
        if "src" not in node.attrib.keys():
            raise exceptions.EmptyNodeContent()
        else:
            imgurl = node.get("src")

        # Organize source
        filename = utils.filename_from_url(imgurl)
        source = "<img src='" + filename + "' orig_src='" + imgurl + "'>" + \
                 "</img><br>\n"

        return source

    def __obtain_caption(self, node: html.HtmlElement) -> str:
        # Prepare text to be analysed
        text = self.__disassembly_text(node)
        text = utils.remove_spaces(text)

        # Check if node have content
        if not text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        source = "<p class='caption'><small>" + text + \
                 "</small></p>\n"

        return source

    def __is_valid_content(self, content: html.HtmlElement) -> bool:
        path = "//p"
        paragraphs = content.xpath(path)
        if len(paragraphs) >= 2:
            return True
        else:
            return False

    def obtain_title(self, element: html.HtmlElement) -> str:
        result = element.xpath(self.title_path)
        if result:
            pre_title = self.__disassembly_text(result[0])
            if pre_title:
                title = pre_title
            else:
                raise exceptions.TitleNotAvailable()
        else:
            raise exceptions.TitleNotAvailable()

        return title

    def obtain_author(self, element: html.HtmlElement) -> str:
        try:
            result = element.xpath(self.author_path)
        except Exception:
            raise exceptions.AuthorNotAvailable()
        if result:
            pre_author = self.__disassembly_text(result[0])
            if pre_author:
                author = pre_author
            else:
                raise exceptions.AuthorNotAvailable()
        else:
            raise exceptions.AuthorNotAvailable()

        return author

    def obtain_date(self, element: html.HtmlElement) -> datetime.datetime:
        try:
            result = element.xpath(self.date_path)
        except Exception:
            raise exceptions.DateNotAvailable()
        if result:
            # Transform to date
            date_text = result[0]
            date = self.__parse_to_date(date_text, self.date_format)
        else:
            raise exceptions.DateNotAvailable()

        return date

    def __parse_to_date(self, date_text: str, date_format: str) \
            -> datetime.datetime:
        date_cleared = utils.remove_spaces(date_text)
        try:
            date = datetime.datetime.strptime(date_cleared, date_format)
        except Exception:
            raise exceptions.DateNotAvailable()
        return date
