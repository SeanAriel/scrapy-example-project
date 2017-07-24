# Very basic spider
# Will start scraping the entire letour.com website because it looks for all links and yields Requests for all of them

import scrapy


class TourDeFranceSpider(scrapy.Spider):
    allowed_domains = ['letour.com']  # scrapy will not follow links that are not part of this domain (like ads)
    start_urls = ['http://www.letour.com/']  # the first url scrapy will request
    name = "tourdefrance1"  # name of our spider to run it with the command line

    def parse(self, response):
        links = response.xpath('//a/@href').extract()  # searches for any a element in the response html and gets the href attribute
        for link in links:
            if link[0] == '/':
                yield scrapy.Request('http://www.letour.com' + link)

