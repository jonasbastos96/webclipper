class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    def __init__(self):
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
