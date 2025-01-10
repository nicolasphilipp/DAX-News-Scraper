import scrapy
from scrapy.selector import Selector
import datetime
from ..items import ContentItem
from ..dbinterface import add_Content, get_ContentByLink
from selenium import webdriver
import locale
import re

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

# make sure all lines end the same
def endSentence(line):
    if line.endswith('.'):
        return line + " "
    elif not line.endswith('. '):
        return line + ". "
    else:
        return line

class Crawler(scrapy.Spider):
    name = "Libertexcrawler"

    allowed_domains = [
        "app.libertex.com",
    ]
    
    start_urls = [
        "https://app.libertex.com/products/indexes/FDAX/",
    ]     

    def parse(self, response):
        # relevant keywords    
        keywords = ["DAX", "Ausblick", "Punkte", "Anlaufziel", "Grenze", "Widerstand", "Widerstände", "Unterstützung", "Ziel", "Marke", "Hindernis", "Richtung"]
        
        # filter relevant pages with regex
        regexp = re.compile(r'#modal_news_.*_FDAX')

        # dynamically load with Selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)    

        driver.get(response.request.url)
        sel = Selector(text=driver.page_source)

        # only enters on first run
        if "https://app.libertex.com/products/indexes/FDAX/" == response.request.url:

            links = sel.xpath("//a/@href").extract()     # extract links

            for l in links:
                if regexp.search(l):
                    newUrl = response.request.url + l       # generate url from starting point + anchor (#modal_news_.*_FDAX)

                    linkPresent = get_ContentByLink(newUrl)        # check with db
                    if not linkPresent:
                        yield self.make_requests_from_url(newUrl)       # send new requests

        # if new articles found
        if regexp.search(response.request.url):
            article = sel.xpath('//div[@class="article"]')
            body = article.xpath('.//div[@class="article-body"]//text()').extract()
            heading = article.xpath('.//h2[@class="section-title"]//text()').extract()
            articleDate = article.xpath('.//span[@class="date"]//text()').extract()

            date = datetime.date.today()
            date = date.strftime('%#d %B %Y')
            time = articleDate[0].split(':')
            hour = time[0][-2:]
            minute = time[1][:2]

            if heading and articleDate:
                if ("Dax im Tagesverlauf" in heading[0] or "Dax (Eurex) (H1) im Tagesverlauf" in heading[0]) and date in articleDate[0]:        # filter articles
                    for x in range(8,17): 
                        if str(x) in hour:      # only work with articles published in opening times
                            input = []

                            for line in body:
                                line = line.replace("\n", " ")
                                line = line.replace("*", "")
                                line = line.strip()

                                if line:
                                    if any(x in line for x in keywords) or any(char.isdigit() for char in line):        # filter lines for keywords
                                        input.append(endSentence(line)) 

                            timestamp = datetime.datetime.now()
                            formattedTimestamp = timestamp.strftime('%d-%m-%Y;%H:%M:%S')
                            splitDate = formattedTimestamp.split(';')

                            content = ContentItem(text=input, url=response.request.url, date=splitDate[0], time=splitDate[1])

                            add_Content(content)       # save in db
                            break
        