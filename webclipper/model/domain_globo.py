import datetime
import re

import requests

from webclipper import exceptions
from webclipper import utils
from webclipper.config import dbconnection
from webclipper.config.logs import logger
from webclipper.model.domain import Domain


class DomainGlobo(Domain):
    def __init__(self):
        super(DomainGlobo, self).__init__()
        query = "SELECT * FROM domain " \
                "WHERE name = 'Globo'"

        result = dbconnection.select(query)

        for row in result:
            self.url = row[0]
            self.name = row[1]
            self.connection_timeout = row[2]
            self.connection_wait = row[3]
            self.connection_attempts = row[4]
            self.connection_agent = row[5]
            self.encoding = row[6]

    def count_news(self, term: str) -> int:
        # Log
        logger.info("Start to count")

        term = "+".join(term.split())
        baseurl = "http://www.globo.com/busca/?q=" + term + "&species=notícias&page="
        factor = 1000
        count = 0
        while factor > 0 and count < 2000:
            current_num = 0
            count += factor
            url = baseurl + str(count)
            try:
                print(url)
                page = self.obtain_element(url)
                nodes = page.xpath(
                    "//span[@class='comum cor-produto atual'][1]")
                current_num = int(utils.remove_spaces(nodes[0].text))
            except exceptions.PageNotFound:
                if count != current_num:
                    count -= factor
                    if factor > 1:
                        factor //= 10
                    else:
                        factor = 0
            # If page have only one page
            except IndexError:
                count = 1
                factor = 0
        tpath = "//ul[@class='resultado_da_busca unstyled']/li"
        try:
            results = page.xpath(tpath)
        # In case of one result page, ignore results
        except UnboundLocalError:
            results = []
        total_news = max(0, count - 1) * 10 + len(results)
        return total_news

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
                                    "second", "seconds", "segundo",
                                    "segundos"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(
                                                 seconds=date_value)
                            elif date_type in (
                                    "minute", "minutes", "minuto", "minutos"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(
                                                 minutes=date_value)
                            elif date_type in (
                                    "hour", "hours", "hora", "horas"):
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(
                                                 hours=date_value)
                            else:
                                data_final = datetime.datetime.today() - \
                                             datetime.timedelta(
                                                 days=date_value)
                        # Pattern 2 (ex: 30 nov. 2014)
                        elif date_detail[2] is not None:
                            data_final = date_detail[2]
                            for pattern in date_pattern:
                                data_final = re.sub(pattern[0], pattern[1],
                                                    data_final,
                                                    flags=re.IGNORECASE)
                            data_final = (
                                datetime.datetime.strptime(data_final,
                                                           "%d %m. %Y", ))
                        # Pattern 3 (ex: Nov 30. 2014)
                        elif date_detail[3] is not None:
                            data_final = date_detail[3]
                            for pattern in date_pattern:
                                data_final = re.sub(pattern[0], pattern[1],
                                                    data_final,
                                                    flags=re.IGNORECASE)
                            data_final = (
                                datetime.datetime.strptime(data_final,
                                                           "%m %d, %Y"))
                        # Pattern 4 (ex: 30/10/2014)
                        else:
                            data_final = (
                                datetime.datetime.strptime(date_detail[4],
                                                           "%d/%m/%Y"))
                        return data_final
                    except ValueError:
                        return None

    def fetch_from_page(self, url: str) -> list:
        news_list = list()
        page = self.obtain_element(url)
        date_path = "./p/span[@class='busca-tempo-decorrido']/text()"
        node_path = "//ul[@class='resultado_da_busca unstyled']/li/div/div"
        link_path = "./a/@href"
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
                    decoded_link = self.decode_link(link[0])
                    news_list.append([data_final, decoded_link])

        return news_list

    def decode_link(self, link_enc: str) -> str:
        link_dec = re.search("u=(.*?)&", link_enc)
        if link_dec:
            link_dec = link_dec.groups()[0]
        link_dec = requests.utils.unquote(link_dec)
        return link_dec

    def list_news(self, term: str) -> list:
        # Log
        logger.info("Starting fetch news from globo from term \"%s\"", term)
        news_list = list()
        news_total = self.count_news(term)
        term = "+".join(term.split())
        baseurl = "http://www.globo.com/busca/?q=" + term + "&species=notícias&page="
        page_total = ((news_total - 1) // 10) + 1

        # Split search for pages
        for count in range(1, page_total + 1):
            logger.info("Progress: %d/%d", (count-1)*10, news_total)
            url = baseurl + str(count)
            fetched_list = self.fetch_from_page(url)

            if fetched_list:
                news_list += fetched_list

        # Log
        logger.info("Fetched links sucessfully")
        return news_list
