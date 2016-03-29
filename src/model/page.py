class Page:
    """ Show to news the possible pages' structures.

        All attributes are lists of strings containing a valid xpath to
        certain part of news.
    """

    def __init__(self):
        self.__heading_tag = str()
        self.__subheading_tag = str()
        self.__text_tag = str()
        self.__subtext_tag = str()
        self.__image_tag = str()
        self.__image_caption_tag = str()
        self.__author_tag = str()
        self.__date_tag = str()
