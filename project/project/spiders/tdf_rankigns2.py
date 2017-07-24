# This scraper will get all the rankings data. Compared to the previous implementation you'll notice that we
# used a different start url here.

import re
import scrapy
from project.items import RankingItem


def get_first(some_list, default=None):
    if len(some_list) > 0:
        return some_list[0]
    return default


class TourDeFranceSpider(scrapy.Spider):
    allowed_domains = ['letour.com']
    start_urls = ['http://www.letour.com/le-tour/2017/us/{}00/classement/bloc-classement-page/ITG.html'.format(x) for x in range(20)]
    name = "tdf_rankings2"

    def parse(self, response):
        stage_nr = int(get_first(re.findall('us/(\d+)00/', response.url)))
        ranking_rows = response.css('table.rankingList tbody tr')
        for row in ranking_rows:
            rank, rider, nr, team, times, gap = row.xpath('.//td/descendant-or-self::*/text()').extract()
            rank_item = RankingItem(
                rider_name=rider,
                rider_nr=nr,
                stage=stage_nr,
                rank=rank
            )
            yield rank_item
