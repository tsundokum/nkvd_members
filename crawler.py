import scrapy
import requests
from w3lib.http import basic_auth_header

NKVD_MEMO_ENTRY = 'https://nkvd.memo.ru/index.php/%D0%9D%D0%9A%D0%92%D0%94:%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'

ROOT = 'https://nkvd.memo.ru'


class RotatingProxyMiddleware(object):
    def __init__(self):
        with open('.proxy.txt') as f:
            self.proxy_address = f.readline().strip()
            self.proxy_login = f.readline().strip()
            self.proxy_pass = f.readline().strip()

    def process_request(self, request, spider):
        request.meta['proxy'] = f'http://{self.proxy_address}'
        request.headers['Proxy-Authorization'] = basic_auth_header(self.proxy_login, self.proxy_pass)

    def process_exception(self, request, exception, spider):
        spider.logger.info(exception)


def fullname(o):
    return o.__module__ + "." + o.__name__


class NKVDMemo(scrapy.Spider):
    name = "nkvdmemo"

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'DOWNLOADER_MIDDLEWARES': {
            fullname(RotatingProxyMiddleware): 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=NKVD_MEMO_ENTRY, callback=self.parse_letters)

    def parse_letters(self, response):
        letters = response.xpath("//a[starts-with(@title, 'НКВД:Именной указатель:')]/@href").extract()
        for let in letters:
            yield response.follow(ROOT + let, self.parse_names)

    def parse_names(self, response):
        names = response.xpath("//div[@class='mw-parser-output']//a[not(starts-with(@title,'НКВД'))]/@href").extract()
        for n in names:
            yield response.follow(ROOT + n, self.parse_destination_table)

    def parse_destination_table(self, response):
        name = response.xpath("//h1[@class='firstHeading']/text()").extract_first()
        bio = ''.join(response.xpath("//p[@class='nkvd-bio']//text()").extract())
        party = ''.join(response.xpath("//p[@class='nkvd-party']//text()").extract())
        nkvd = ''.join(response.xpath("//p[@class='nkvd-nkvd']//text()").extract())
        repres = ''.join(response.xpath("//p[@class='nkvd-repr']//text()").extract())
        info = ''.join(response.xpath("//p[@class='nkvd-info']//text()").extract())

        designation_table = response.xpath("//table[@class='nkvd-designation-table']/tr[starts-with(@id, 'mw-customcollapsible-designation')]")
        designations = []
        for row in designation_table:
            marker = row.xpath(".//td[@class='nkvd-table-marker']/span/@title").extract_first()
            prep = row.xpath(".//td[@class='nkvd-table-preposition']//text()").extract_first()
            date = row.xpath(".//td[@class='nkvd-table-date']//text()").extract_first()
            pos = row.xpath(".//td[@class='nkvd-table-position']//text()").extract_first()
            source = row.xpath(".//td[@class='nkvd-table-source']//text()").extract_first()
            unit = row.xpath(".//td[@class='nkvd-table-unit']//text()").extract_first()
            designations.append([marker, prep, date, pos, source, unit])

        rank_table = response.xpath("//table[@class='nkvd-rank-table']/tr[starts-with(@id, 'mw-customcollapsible-rank')]")
        ranks = []
        for row in rank_table :
            marker = row.xpath(".//td[@class='nkvd-table-marker']/span/@title").extract_first()
            prep = row.xpath(".//td[@class='nkvd-table-preposition']//text()").extract_first()
            date = row.xpath(".//td[@class='nkvd-table-date']//text()").extract_first()
            rank = row.xpath(".//td[@class='nkvd-table-rank']//text()").extract_first()
            source = row.xpath(".//td[@class='nkvd-table-source']//text()").extract_first()
            ranks.append([marker, prep, date, rank, source])

        yield {"link": response.request.url,
               "name": name,
               "bio": bio,
               "party": party,
               "nkvd": nkvd,
               "repr": repres,
               "info": info,
               "designations": designations,
               "ranks": ranks}
