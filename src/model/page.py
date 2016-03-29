class Page:
    """ Show to news the possible pages' structures.

        All attributes are lists of strings containing a valid xpath to
        certain part of news.
    """

    def __init__(self):
        self.headingTag = str()
        self.subheadingTag = str()
        self.textTag = str()
        self.subtextTag = str()
        self.imageTag = str()
        self.image_captionTag = str()
        self.authorTag = str()
        self.dateTag = str()
