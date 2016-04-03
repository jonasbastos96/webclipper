from webclipper.model.domain import Domain
import requests
import time


class DomainUol(Domain):
    def __init__(self):
        super(Domain, self).__init__()

    def obtain_source(self, url: str()):
        # Initial parameters
        attempts = 0
        src_page = str()
        bad_status_code = (403, 404)

        # Capture of source
        while not src_page:
            attempts += 1
            try:
                src_page = requests.get(url, headers=self.connection_header,
                                        timeout=self.connection_timeout)
                # If page can't be captured
                if src_page.status_code in bad_status_code:
                    # In case wasn't found, raise an error
                    if src_page.status_code == 404:
                        err = "Page not found"
                        raise requests.HTTPError(err)
                    # Clear what was found
                    src_page = str()

            # In case of an connection error, ignore and try again
            except requests.ConnectionError:
                pass

            if attempts % 100 == 0:
                time.sleep(attempts//10)

        # Change encode
        src_page.encoding = self.encoding
        return src_page.text
