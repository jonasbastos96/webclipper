from datetime import datetime

from webclipper.config import dbconnection
from webclipper.model.domain import Domain


class DomainElmundo(Domain):
    def __init__(self):
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

    def list_news(self, term: str):
        baseurl = "http://ariadna.elmundo.es/buscador/archivo.html?n=50&b_avanzada=elmundoes&q="
        begin_date = datetime(2000, 1, 1)
        end_date = datetime.now()

        year_range = range(begin_date.year, end_date.year + 1)

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

            for month in month_range:
                print("ok")
