# This is a naive implementation to scrape the rankings data. However, it will fail.

import re
import scrapy
from project.items import RankingItem


def get_first(some_list, default=None):
    if len(some_list) > 0:
        return some_list[0]
    return default


class TourDeFranceSpider(scrapy.Spider):
    allowed_domains = ['letour.com']
    start_urls = ['http://www.letour.com/le-tour/2017/us/stage-{}/classifications.html'.format(x) for x in range(20)]
    name = "tdf_rankings1"

    def parse(self, response):
        ranking_rows = response.css('table.rankingList tr')
        stage_nr = get_first(re.findall('stage-(\d+)', response.url))
        for row in ranking_rows:
            rank, rider, nr, team, times, gap = row.xpath('string(.//td)').extract()
            rank_item = RankingItem(
                rider_name=rider,
                stage=stage_nr,
                rank=rank
            )
            yield rank_item
