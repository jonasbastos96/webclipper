from webclipper.model.domain import Domain


class DomainElmundo(Domain):
    def __init__(self, **kwargs):
        super(DomainElmundo, self).__init__(**kwargs)

    def download_image(self, url: str, filename: str = None) -> str:
        # Check if url is incomplete and add an "http:" on begining
        if not url.startswith("http:"):
            url = "http:" + url

        # Call Domain's method to download the image normally
        return super(DomainElmundo, self).download_image(url, filename)
