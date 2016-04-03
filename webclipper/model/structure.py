class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    def __init__(self):
        self.heading_tag = str()
        self.subheading_tag = str()
        self.text_tag = str()
        self.subtext_tag = str()
        self.image_tag = str()
        self.caption_tag = str()
        self.author_tag = str()
        self.date_tag = str()
