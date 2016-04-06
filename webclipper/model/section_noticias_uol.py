from lxml import html

from webclipper.model.section import Section


class SectionNoticiasUol(Section):
    def __init__(self, url: str = None):
        super(SectionNoticiasUol, self).__init__(url)

    def filter_element(self, element: html.HtmlElement):
        # Add suport to caption
        nodes = element.xpath("//p[@class='wp-caption-text']")
        for node in nodes:
            node.tag = "figcaption"
            node.tag = "figcaption"
