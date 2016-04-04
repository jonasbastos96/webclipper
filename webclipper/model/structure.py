class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    def __init__(self, **kwargs):
        self.title_tag = str()
        self.heading_tag = str()
        self.text_tag = str()
        self.subtext_tag = str()
        self.image_tag = str()
        self.caption_tag = str()
        self.title_path = str()
        self.author_path = str()
        self.date_path = str()
        self.content_path = str()
        self.date_format = str()

        if "row" in kwargs.keys():
            self.title_tag = kwargs["row"][1]
            self.heading_tag = kwargs["row"][2]
            self.text_tag = kwargs["row"][3]
            self.subtext_tag = kwargs["row"][4]
            self.image_tag = kwargs["row"][5]
            self.caption_tag = kwargs["row"][6]
            self.title_path = kwargs["row"][7]
            self.author_path = kwargs["row"][8]
            self.date_path = kwargs["row"][9]
            self.content_path = kwargs["row"][10]
            self.date_format = kwargs["row"][11]
