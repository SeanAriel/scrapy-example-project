import scrapy


class RiderItem(scrapy.Item):
    name = scrapy.Field()
    team = scrapy.Field()
    country = scrapy.Field()
    birth_date = scrapy.Field()
    number = scrapy.Field()


class RankingItem(scrapy.Item):
    rider_name = scrapy.Field()
    rider_nr = scrapy.Field()
    stage = scrapy.Field()
    rank = scrapy.Field()