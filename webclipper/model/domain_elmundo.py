from datetime import datetime

import requests

from webclipper import exceptions
from webclipper.config import dbconnection
from webclipper.config.logs import logger
from webclipper.model.domain import Domain


class DomainElmundo(Domain):
    def __init__(self):
        super(DomainElmundo, self).__init__()
        query = "SELECT * FROM domain " \
                "WHERE domain.url = 'http://www.elmundo.es/'"
        result = dbconnection.select(query)

        for row in result:
            self.url = row[0]
            self.name = row[1]
            self.connection_timeout = row[2]
            self.connection_wait = row[3]
            self.connection_attempts = row[4]
            self.connection_agent = row[5]
            self.encoding = row[6]

    def download_image(self, url: str, filename: str = None) -> str:
        # Check if url is incomplete and add an "http:" on begining
        if not url.startswith("http:"):
            url = "http:" + url

        # Call Domain's method to download the image normally
        return super(DomainElmundo, self).download_image(url, filename)

    def __fetch_from_page(self, url: str) -> list:
        news_list = list()
        element = self.obtain_element(url)
        # Path in source
        node_path = "//ul[@class='lista_resultados']/li[not(@*)]"
        date_path = "./div/ul/li/span[@class='fecha']/text()[1]"
        link_path = "./h3/a/@href[1]"
        # Get nodes from source
        nodes = element.xpath(node_path)

        # Subdivide in nodes
        for node in nodes:
            # Retrieve date of news
            date_node = node.xpath(date_path)
            link_node = node.xpath(link_path)
            # Check if have date
            if date_node and link_node:
                date_news = datetime.strptime(date_node[0], "%d/%m/%Y")
                url_news = link_node[0]
                # Append news on list, with date and url
                news_list.append([date_news, url_news])

        return news_list

    def list_news(self, term: str) -> list:
        logger.info("Starting fetch news from elmundo from term \"%s\"", term)
        news_list = list()
        term_enc = requests.utils.quote(term, encoding="cp1252")
        term_enc = "+".join(term_enc.split())
        baseurl = "http://ariadna.elmundo.es/buscador/archivo.html?n=50&b_avanzada=elmundoes&q=" + term_enc
        begin_date = datetime(2000, 1, 1)
        end_date = datetime.now()

        year_range = range(begin_date.year, end_date.year + 1)

        # Split in years
        for year in year_range:
            month_range = range

            if year == begin_date.year:
                if year == end_date.year:
                    month_range = range(begin_date.month, end_date.month + 1)
                else:
                    month_range = range(begin_date.month, 12 + 1)
            elif year == end_date:
                month_range = range(1, end_date.month + 1)
            else:
                month_range = range(1, 12 + 1)

            # Split in months
            for month in month_range:
                logger.info("Fetching list in %d/%d", year, month)
                # Mount a new base url, according year and month
                baseurl2 = baseurl
                baseurl2 += "&parametric_year=" + str(year)
                baseurl2 += "&parametric_month=" + str(month)

                # Get elements from first page on search
                try:
                    element = self.obtain_element(baseurl2 + "&i=1")
                except exceptions.PageNotFound:
                    continue

                # Count number of news found
                amount_news_path = "//span[@class='numero_resultados']/strong/text()"
                amount_news = element.xpath(amount_news_path)

                if not amount_news:
                    continue

                amount_news = int(amount_news[0])

                # Split search by pages
                for count in range(1, amount_news + 1, 50):
                    logger.info("Progress: %d/%d", count - 1, amount_news)
                    url = baseurl2 + "&i=" + str(count)
                    logger.debug("Starting fetch list of news from %s", url)
                    fetched_list = self.__fetch_from_page(url)
                    if fetched_list:
                        news_list += fetched_list

                logger.info("Fetched links sucessfully")

        return news_list
