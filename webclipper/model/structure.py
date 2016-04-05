class Structure:
    """
    Show to news the possible pages' structures.

    All attributes are lists of strings containing a valid xpath to
    certain part of news.
    """

    # Class atributes
    HEAD_CONTENT = "<head>\n" \
                   "<style>\n" \
                   ".main-content {text-align: justify; text-indent: 50px;}\n" \
                   ".image-caption {text-align: center;}\n" \
                   "img {display: block; margin: 0 auto;}\n" \
                   "</style>\n" \
                   "<meta charset='utf-8'>\n" \
                   "<head>\n"

    # Instance attributes
    def __init__(self, **kwargs):
        self.title_tag = list
        self.heading_tag = list
        self.text_tag = list
        self.subtext_tag = list
        self.image_tag = list
        self.caption_tag = list
        self.title_path = str
        self.author_path = str
        self.date_path = str
        self.content_path = str
        self.date_format = str

        if "row" in kwargs.keys():
            self.title_tag = kwargs["row"][1].split(",")
            self.heading_tag = kwargs["row"][2].split(",")
            self.text_tag = kwargs["row"][3].split(",")
            self.subtext_tag = kwargs["row"][4].split(",")
            self.image_tag = kwargs["row"][5].split(",")
            self.caption_tag = kwargs["row"][6].split(",")
            self.title_path = kwargs["row"][7]
            self.author_path = kwargs["row"][8]
            self.date_path = kwargs["row"][9]
            self.content_path = kwargs["row"][10]
            self.date_format = kwargs["row"][11]
