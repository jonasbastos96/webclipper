import requests
import time


class Domain(object):
    def __init__(self):
        self.url = str()
        self.name = str()
        self.connection_timeout = int()
        self.connection_wait = int()
        self.connection_attempts = int()
        self.connection_header = str()
        self.encoding = str()

    def obtain_source(self, url: str()):
        # Initial parameters
        limit = self.connection_attempts
        wait = self.connection_wait
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

            # If attempts of get the source is higher than limit, raise an error
            if attempts > limit > 0:
                err = "Limit of attempts reached"
                raise requests.HTTPError(err)

            if attempts > 1:
                time.sleep(wait)

        # Change encode
        src_page.encoding = self.encoding
        return src_page.text
