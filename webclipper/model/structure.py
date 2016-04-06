from lxml import html

from webclipper import exceptions
from webclipper import utils


class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    # Class atributes
    # TODO ajust charset for each url
    HEAD_CONTENT = "<head>\n" \
                   "<style>\n" \
                   ".main-content {text-align: justify; text-indent: 50px;}\n" \
                   ".caption {text-align: center;}\n" \
                   "img {display: block; margin: 0 auto;}\n" \
                   "</style>\n" \
                   "<meta charset='utf-8'>\n" \
                   "<head>\n"

    # Instance attributes
    def __init__(self, **kwargs):
        self.title_tag = list()
        self.heading_tag = list()
        self.text_tag = list()
        self.image_tag = list()
        self.caption_tag = list()
        self.title_path = str()
        self.author_path = str()
        self.date_path = str()
        self.content_path = str()
        self.date_format = str()

        if "row" in kwargs.keys():
            if kwargs["row"][1]:
                self.title_tag = kwargs["row"][1].split(",")
            if kwargs["row"][2]:
                self.heading_tag = kwargs["row"][2].split(",")
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
        nodes = element.xpath(self.content_path)

        for node in nodes:
            try:
                if node.tag in self.heading_tag:
                    source += self.__obtain_heading(node)
                elif node.tag in self.text_tag:
                    source += self.__obtain_text(node)
                elif node.tag in self.image_tag:
                    source += self.__obtain_image(node)
                elif node.tag in self.caption_tag:
                    source += self.__obtain_caption(node)
            except exceptions.EmptyNodeContent:
                pass

        content = html.fromstring(source)
        if not self.__is_valid_content(content):
            raise exceptions.UnsupportedURL()

        return content

    def __obtain_heading(self, node: html.HtmlElement) -> str:
        # Check if node have content
        if not node.text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        text_formated = utils.remove_spaces(node.text)
        source = "<h1>" + text_formated + "</h1>\n"

        return source

    def __obtain_text(self, node: html.HtmlElement) -> str:
        text = self.__disassembly_text(node)

        # Check if disassembled text have content
        if not text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        text = utils.remove_spaces(text)
        source = "<p class='main-content'>" + text + "</p>\n"

        return source

    def __disassembly_text(self, node: html.HtmlElement, is_first=True) -> str:
        text = str()
        if node.text:
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
        # Check if node have content
        if not node.text:
            raise exceptions.EmptyNodeContent()

        # Organize source
        text_formated = utils.remove_spaces(node.text)
        source = "<p class='caption'><small>" + text_formated + \
                 "</small></p>\n"

        return source

    def __is_valid_content(self, content: html.HtmlElement) -> bool:
        path = "//p"
        paragraphs = content.xpath(path)
        if len(paragraphs) >= 2:
            return True
        else:
            return False
