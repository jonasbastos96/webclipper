import requests


class Domain:
    def __init__(self):
        self.url = str()
        self.name = str()
        self.connection_timeout = int()
        self.connection_wait = int()
        self.connection_attempts = int()
        self.connection_header = str()

    def obtain_source(self, url: str()):
        # Initial parameters
        limit = self.connection_attempts
        attempts = 0
        src_page = str()
        bad_status_code = (403, 404)

        # Capture of source
        while not src_page:
            attempts += 1
            try:
                src_page = requests.get(url, headers=self.connection_header,
                                        timeout=self.connection_timeout)
                # If page can't be captured, clear what was found
                if src_page.status_code in bad_status_code:
                    src_page = str()
                    # In case wasn't found, raise an error
                    if src_page.status_code == 404:
                        err = "Page not found"
                        raise requests.HTTPError(err)

            # In case of an connection error, ignore and try again
            except requests.ConnectionError:
                pass

            # If attempts of get the source is higher than limit, raise an error
            if attempts > limit:
                err = "Limit of attempts reached"
                raise requests.HTTPError(err)

        return src_page
