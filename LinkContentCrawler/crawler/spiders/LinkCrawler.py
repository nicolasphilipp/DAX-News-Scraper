import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from ..items import LinkItem
from ..dbinterface import get_ContentByLink
import datetime
import html2text

class Crawler(CrawlSpider):
    name = "Linkcrawler"

    allowed_domains = [
        "www.onvista.de",
        "www.dailyfx.com", 
        "finanzmarktwelt.de", 
        "de.investing.com",
        "www.boerse-online.de", 
        "www.boerse-daily.de", 
        "www.godmode-trader.de",
    ]

    start_urls = [
        "https://www.onvista.de/news/alle-news?searchTerm=dax&dateRange=&orderBy=&min=&max=&doFilter=true&doFilterSubmit=Filter+anwenden",
        "https://www.dailyfx.com/deutsch/marktausblick",
        "https://finanzmarktwelt.de/dax-daily-keine-guten-vorzeichen-wochenausblick-189838/",
        "https://de.investing.com/members/contributors/205840426/opinion",
        "https://www.boerse-online.de/maerkte/dax-chartanalyse",
        "https://www.boerse-daily.de/news-analysen-insight",
        "https://www.godmode-trader.de/indizes/dax-performance-index-kurs,133962",
    ]     

    custom_settings = {
        'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'LOG_LEVEL': 'INFO', 
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 15,
        'REDIRECT_ENABLED': True,
        'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
    }

    rules = (        
        Rule(LinkExtractor(deny=(r'\.pdf', r'\?pdf')), callback='parse', follow=False),         # don't follow pdfs
    )

    def parse(self, response):
        url = response.url
        regex = re.compile(r'\bfacebook\b | \btwitter\b | \bgoogle\b | \bwhatsapp\b | \bkontakt\b | \b\?\b | \blivestream\b | \bvideo\b', flags=re.I | re.X)     # blacklist for links
        x = re.search(regex, url)

        # predefined regex for targeted sites
        boerseO_regex = re.compile(r'^(?=.*www\.boerse-online\.de/nachrichten/ressort/maerkte/dax-chartanalyse).+$')
        boerseD_regex = re.compile(r'^(?=.*www\.boerse-daily\.de/boersen-nachrichten/insight)(?=.*dax).*$')
        godmode_regex1 = re.compile(r'^(?=.*www\.godmode-trader\.de/artikel/tagesausblick)(?=.*dax).*$')
        godmode_regex2 = re.compile(r'^(?=.*www\.godmode-trader\.de/analyse/dax-tagesausblick).+$')
        onvista_regex1 = re.compile(r'^(?=.*www\.onvista\.de/news/dax).*$')     
        onvista_regex2 = re.compile(r'^(?=.*www\.onvista\.de/news/tagesausblick)(?=.*dax).*$')
        investing_regex = re.compile(r'^(?=.*de\.investing\.com/analysis/technische-analyse-dax).+$')
        dailyfx_regex = re.compile(r'^(?=.*www\.dailyfx\.com/deutsch/devisenhandel/fundamental/tagliche_analyse)(?=.*DAX-Prognose).*$')
        finanzmarktwelt_regex = re.compile(r'^(?=.*finanzmarktwelt\.de/dax-daily).+$')

        regexList = [boerseO_regex, boerseD_regex, godmode_regex1, godmode_regex2, onvista_regex1, onvista_regex2, investing_regex, dailyfx_regex, finanzmarktwelt_regex]

        if x is None:
            if any(regex.match(url) for regex in regexList):
                if "finanzmarktwelt.de" in url and "return" in url:         # special case for finanzmarktwelt.de
                    url = url.split("return=",1)[1]

                linkPresent = get_ContentByLink(url)       # check with db
                if not linkPresent:
                    item = LinkItem(link_url=url)
                    yield item 
        