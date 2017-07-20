import scrapy


class TourDeFranceSpider(scrapy.Spider):
    allowed_domains = ['letour.com']
    start_urls = ['http://www.letour.com/le-tour/2017/us/starters.html']
    name = "tourdefrance2"

    def parse(self, response):
        rider_links = response.css('ul.equipes table').xpath('.//a/@href').extract()
        for link in rider_links:
            if link[0] == '/':
                yield scrapy.Request('http://www.letour.com' + link)