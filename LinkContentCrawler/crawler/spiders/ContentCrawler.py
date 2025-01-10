import scrapy
from scrapy import Request
import datetime
from ..items import ContentItem
import json
from ..dbinterface import add_Content
import html2text

converter = html2text.HTML2Text()
converter.ignore_links = True

# make sure all lines end the same
def endSentence(line):
    if line.endswith('.'):
        return line + " "
    elif not line.endswith('. '):
        return line + ". "
    else:
        return line

# format line
def processLine(line):
    textToAppend = converter.handle(line).strip()
    textToAppend = textToAppend.replace("\n", " ")
    textToAppend = textToAppend.replace("*", "")

    return textToAppend

# format table
def processTable(line):
    textToAppend = converter.handle(line).strip()
    textToAppend = textToAppend.replace("|", "")
    textToAppend = textToAppend.replace("*", "")
    textToAppend = ' '.join(textToAppend.split())
    
    return textToAppend

class Crawler(scrapy.Spider):
    name = "Contentcrawler"

    static_linklist = [
        "https://admiralmarkets.com/de/analysen/dax30-tages-updates"
    ]  

    # don't allow redirects
    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta = {
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    def start_requests(self):
        # input filename is provided by commandline
        f = open(self.inputfile, "r", encoding='utf-8')
        data = json.loads(f.read())
        f.close()

        url_list = []

        # save links from file in array
        for entry in data:
            url_list.append(entry['link_url'])

        # add static links
        for url in self.static_linklist:
            url_list.append(url);        

        # make requests
        for url in url_list:
            yield self.make_requests_from_url(url)
            #yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # relevant keywords 
        keywords = ["DAX", "Ausblick", "Punkte", "Anlaufziel", "Grenze", "Widerstand", "Widerstände", "Unterstützung", "Ziel", "Marke", "Hindernis", "Richtung"]  

        text = []
        content = response

        # select content by xpath
        if "finanzmarktwelt.de" in response.request.url:            
            content = response.xpath('//div[@class="entry-content"]') 
        elif "onvista.de" in response.request.url:           
            content = response.xpath('//div[@id="newsContentContainer"]')
        elif "boerse-online.de" in response.request.url:
            content = response.xpath('//div[@id="scroll"]')
        elif "boerse-daily.de" in response.request.url:
            content = response.xpath('//div[@id="nachrichten-leser"]')
        elif "admiralmarkets.com" in response.request.url:
            content = response.xpath('//article')
        elif "dailyfx.com" in response.request.url:
            content = response.xpath('//div[@class="dfx-articleBody"]')
        elif "investing.com" in response.request.url:
            content = response.xpath('//div[@class="WYSIWYG articlePage"]')

        for line in content.xpath('.//p//text()').extract():       
            text.append(processLine(line))

        for line in content.xpath('.//ul//text()').extract():     
            text.append(processLine(line))

        # take table from boerse-online
        if "boerse-online.de" in response.request.url or "onvista.de" in response.request.url:
            for line in content.xpath('.//tr').extract():
                text.append(processTable(line))
        elif "boerse-daily.de" in response.request.url:
            for line in content.xpath('//div[@class="chart-meta"]//tr').extract():  
                text.append(processTable(line))

        filteredInput = []

        # filter content
        for line in text:
            if "finanzmarktwelt.de" in response.request.url or "investing.com" in response.request.url:
                if any(x in line for x in keywords) or any(char.isdigit() for char in line):  
                    filteredInput.append(endSentence(line))
            else:
                if any(x in line for x in keywords):
                    filteredInput.append(endSentence(line))

        timestamp = datetime.datetime.now()
        formattedTimestamp = timestamp.strftime('%d-%m-%Y;%H:%M:%S')
        splitDate = formattedTimestamp.split(';')

        if "admiralmarkets.com" in response.request.url:        # special case for admiralmarkets
            date = datetime.date.today()
            if date.isoweekday() in range(1, 8):
                saveUrl = response.request.url + "#" + str(date)
                content = ContentItem(text=filteredInput, url=saveUrl, date=splitDate[0], time=splitDate[1])
            else:
                return     
        else:
            content = ContentItem(text=filteredInput, url=response.request.url, date=splitDate[0], time=splitDate[1])
       
        add_Content(content)     # save in db