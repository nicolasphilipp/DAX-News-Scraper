# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    text = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()

    def __str__(self):
        output = self['url'] + ";;"
        for line in self['text']:
            output += line

        return output + ";;" + self['date'] + ";;" + self['time']

class LinkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    link_url = scrapy.Field()

    pass
    