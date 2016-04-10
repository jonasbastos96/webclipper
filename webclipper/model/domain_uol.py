import difflib
import time
import re
import datetime
from itertools import chain

from lxml import html
import requests

from webclipper.config import dbconnection
from webclipper.config.logs import logger
from webclipper.model.domain import Domain
from webclipper import utils


class DomainUol(Domain):
    def __init__(self):
        super(DomainUol, self).__init__()
        query = "SELECT * FROM domain " \
                "WHERE name = 'Uol'"

        result = dbconnection.select(query)

        for row in result:
            self.url = row[0]
            self.name = row[1]
            self.connection_timeout = row[2]
            self.connection_wait = row[3]
            self.connection_attempts = row[4]
            self.connection_agent = row[5]
            self.encoding = row[6]

    def obtain_source(self, url: str()):
        # Initial parameters
        attempts = 0
        src_page = str()
        bad_status_code = (403, 404)

        # Capture of source
        while not src_page:
            attempts += 1
            try:
                headers = {"User-Agent": self.connection_agent}
                src_page = requests.get(url, headers=headers,
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
                time.sleep(attempts // 10)

        # Change encode
        src_page.encoding = self.encoding
        return src_page.text

    # TODO Urgent refactor and analysis
    def __count_news(self, term: str) -> int:
        # Log
        logger.info("Starting to count how many news have in Uol domain about "
                    "{term} term".format(term=term))
        term = "+".join(term.split())
        baseurl = "http://busca.uol.com.br/uol/?q=" + term + "&sort=date&start="
        factor = 100
        count = 0
        previous_page = None
        first_page = self.obtain_element(baseurl + "1")
        tpath = "//ul[@class='results organic']/li"
        results = first_page.xpath(tpath)
        first_page = html.tostring(first_page)

        if len(results) == 0:
            return 0
        elif len(results) < 10:
            return len(results)
        else:
            while factor > 1:
                if count + factor >= 1000:
                    factor //= 10
                    previous_page = None
                else:
                    count += factor
                    url = baseurl + str(count)
                    # Log
                    logger.info("Analysing page {num}...".format(num=count))
                    current_page = self.obtain_element(url)

                    tpath = "//ul[@class='results organic']/li"
                    results = current_page.xpath(tpath)

                    current_page = html.tostring(current_page)

                    if not previous_page:
                        previous_page = current_page
                    else:
                        similarity = difflib.SequenceMatcher(None,
                                                             previous_page,
                                                             current_page).ratio()
                        previous_page = current_page
                        if similarity > 0.85:
                            count -= factor * 2
                            factor //= 10
                            if factor is not 1:
                                previous_page = None
            if count == 0:
                similarity = difflib.SequenceMatcher(None, previous_page,
                                                     first_page).ratio()
                if similarity > 0.85:
                    return 10
                else:
                    results = previous_page.xpath(tpath)
                    return 10 + len(results)

        # Log
        amount = count + 10 + len(results)
        logger.info("Successufully count pages. Total of {num}"
                    .format(num=amount))
        return amount

    def __decode_date(self, node, date_path):
        element = node.xpath(date_path)
        date_regex = "([0-9]?[0-9]) ((?:segundo|second|minuto|minute|hora|hour|dia|day)[s]?)|" \
                     "([0-9]?[0-9] [A-z]{3}. [0-9]{4})|" \
                     "([A-z]{3} [0-9]?[0-9], [0-9]{4})|" \
                     "([0-9]?[0-9]/[0-9]{2}/[0-9]{4})"
        # If have date
        if element:
            node_date = utils.remove_spaces(element[0])
            # Check if captured information is, indeed, a date
            if len(node_date) <= 20:
                date_detail = re.search(date_regex, node_date)
                # If date is in a valid pattern, check pattern used
                if date_detail:
                    date_pattern = [
                        ["((?:jan|jan))", "1"],
                        ["((?:fen|feb))", "2"],
                        ["((?:mar|mar))", "3"],
                        ["((?:abr|apr))", "4"],
                        ["((?:mai|may))", "5"],
                        ["((?:jun|jun))", "6"],
                        ["((?:jul|jul))", "7"],
                        ["((?:ago|agu))", "8"],
                        ["((?:set|sep))", "9"],
                        ["((?:out|oct))", "10"],
                        ["((?:nov|nov))", "11"],
                        ["((?:dez|dec))", "12"]
                    ]
                    date_detail = date_detail.groups()
                    # Pattern 1 (ex: "2 days ago")
                    try:
                        if date_detail[0] is not None \
                                and date_detail[1] is not None:
                            date_value = int(date_detail[0])
                            date_type = date_detail[1]
                            if date_type in (
                            "second", "seconds", "segundo", "segundos"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(seconds=date_value)
                            elif date_type in (
                            "minute", "minutes", "minuto", "minutos"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(minutes=date_value)
                            elif date_type in (
                            "hour", "hours", "hora", "horas"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(hours=date_value)
                            else:
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(days=date_value)
                        # Pattern 2 (ex: 30 nov. 2014)
                        elif date_detail[2] is not None:
                            data_final = date_detail[2]
                            for pattern in date_pattern:
                                data_final = re.sub(pattern[0], pattern[1],
                                                    data_final,
                                                    flags=re.IGNORECASE)
                            data_final = (
                            datetime.datetime.strptime(data_final, "%d %m. %Y", ))
                        # Pattern 3 (ex: Nov 30. 2014)
                        elif date_detail[3] is not None:
                            data_final = date_detail[3]
                            for pattern in date_pattern:
                                data_final = re.sub(pattern[0], pattern[1],
                                                    data_final,
                                                    flags=re.IGNORECASE)
                            data_final = (
                            datetime.datetime.strptime(data_final, "%m %d, %Y"))
                        # Pattern 4 (ex: 30/10/2014)
                        else:
                            data_final = (
                            datetime.datetime.strptime(date_detail[4], "%d/%m/%Y"))
                        return data_final
                    except ValueError:
                        return None

    def fetch_from_page(self, url: str) -> list:
        news_list = list()
        page = self.obtain_element(url)
        date_path = "./dd/text()[1]"
        node_path = "//ul[@class='results organic']/li/dl"
        link_path = "./dt/a/@href[1]"
        nodes = page.xpath(node_path)

        # Split search by links found
        for sites in nodes:
            data_final = self.__decode_date(sites, date_path)
            # If exists a data
            if data_final:
                link = sites.xpath(link_path)
                # And if the news have a capturable link
                # if link and link in get_supported():
                if link:
                    # Append to list of capturable sites
                    news_list.append([data_final, link[0]])

        return news_list

    def list_news(self, term: str) -> list():
        # Log
        logger.info("Starting fetch news from uol from term \"%s\"", term)
        news_list = list()
        news_total = self.__count_news(term)
        term = "+".join(term.split())
        baseurl = "http://busca.uol.com.br/uol/?q=" + term + "&sort=date&start="
        search_range = chain(range(1, 2), range(10, news_total, 10))

        # Split search for pages
        for count in search_range:
            logger.info("Progress: %d/%d", count, news_total)
            url = baseurl + str(count)
            fetched_list = self.fetch_from_page(url)

            if fetched_list:
                news_list += fetched_list

        # Log
        logger.info("Fetched links sucessfully")
        return news_list

