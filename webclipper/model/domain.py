from webclipper import exceptions
import re
import shutil
import time
import requests
from lxml import html


class Domain(object):
    def __init__(self, **kwargs):
        self.url = str()
        self.name = str()
        self.connection_timeout = int()
        self.connection_wait = int()
        self.connection_attempts = int()
        self.connection_header = str()
        self.encoding = str()

        if "row" in kwargs.keys():
            self.url = kwargs["row"][0]
            self.name = kwargs["row"][1]
            self.connection_timeout = kwargs["row"][2]
            self.connection_wait = kwargs["row"][3]
            self.connection_attempts = kwargs["row"][4]
            self.connection_header = kwargs["row"][5]
            self.encoding = kwargs["row"][6]

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
                        raise exceptions.PageNotFound()
                    # Clear what was found
                    src_page = str()

            # In case of connection timeout, raise an error
            except requests.Timeout:
                raise exceptions.Timeout()
            # In case of an connection error, ignore and try again
            except requests.ConnectionError:
                pass

            # If attempts of get the source is higher than limit, raise an error
            if attempts > limit > 0:
                raise exceptions.AttemptsError()

            if attempts > 1:
                time.sleep(wait)

        # Change encode
        src_page.encoding = self.encoding
        return src_page.text

    def obtain_element(self, url=str()):
        source = self.obtain_source(url)
        element = html.fromstring(source)
        return element

    def download_image(self, url=str()):
        image_dir = str()
        try:
            # image to be saved
            imgtosave = requests.get(url, stream=True)

            # Filename according original name
            filename = re.search("([^/?#]*\.[^/?#]*?$)", url)
            filename = filename.groups()[0]

            # Saving image
            if imgtosave.status_code == 200:
                with open("..\\temp\\" + filename, "wb") as file:
                    file.raw.decode_content = True
                    shutil.copyfileobj(imgtosave.raw, file)

            # Directory of saved image
            image_dir = "..\\webclipper\\temp\\" + filename
        except (Exception, requests.HTTPError):
            raise exceptions.DownloadError()

        if not image_dir:
            raise exceptions.DownloadError()

        return image_dir
