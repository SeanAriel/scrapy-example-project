# Add a callback to the rider pages Requests
# Those pages will now be parsed with parse_rider_page
# We also configured a pipeline here

import scrapy
from project.items import RiderItem


def get_first(some_list, default=None):
    """
    Helper function: gets first item of a list if the list has 1 or more elements. Otherwise, the default
    value is returned
    """
    if len(some_list) > 0:
        return some_list[0]
    return default


class TourDeFranceSpider(scrapy.Spider):
    allowed_domains = ['letour.com']
    start_urls = ['http://www.letour.com/le-tour/2017/us/starters.html']
    name = "tourdefrance3"
    custom_settings = {
        'ITEM_PIPELINES': {
            'project.pipelines.TestPipeline': 100
        }
    }

    def parse(self, response):
        rider_links = response.css('ul.equipes table').xpath('.//a/@href').extract()
        for link in rider_links:
            if link[0] == '/':
                yield scrapy.Request('http://www.letour.com' + link, callback=self.parse_rider_page)

    def parse_rider_page(self, response):
        # There are two ways to get all the text in an element and its children:
        #    1. ./descendant-or-self::*/text()
        #    2. string(./descendant-or-self::*)
        #
        # You can try both in the scrapy shell: scrapy shell http://www.letour.com/le-tour/2017/us/riders/ag2r-la-mondiale/bakelants-jan.html

        name_raw = get_first(response.css('span.riderInfos__personName').xpath('string(./descendant-or-self::*)').extract(), '')
        name = name_raw.strip()

        team_raw = get_first(response.css('span.riderInfos__team__name').xpath('string(./descendant-or-self::*)').extract(), '')
        team = team_raw.strip()

        country_raw = get_first(response.css('span.riderInfos__country__name').xpath('string(./descendant-or-self::*)').extract(), '')
        country = country_raw.strip()

        birth_date_raw = get_first(response.css('span.riderInfos__birth').xpath('string(./descendant-or-self::*)').extract(), '')
        birth_date = birth_date_raw.strip()

        number_raw = get_first(response.css('span.riderInfos__bib__number').xpath('string(./descendant-or-self::*)').extract(), '')
        number = number_raw.strip()

        rider = RiderItem(
            name=name,
            team=team,
            country=country,
            birth_date=birth_date,
            number=number
        )

        yield rider
