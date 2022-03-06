import scrapy
import re
from movieScrapy import settings
from movieScrapy.items import TopMovieItem
from movieScrapy.utils.redisUtils import RedisUtil


class TopMovieItemSpider(scrapy.Spider):
    name = 'top_movie_item_spider'

    allow_domain = ['www.douban.com', 'movie.douban.com']

    custom_settings = {
        'ITEM_PIPELINES': {'movieScrapy.pipelines.TopMoviePipeLine': 300}
    }

    default_headers = settings.DEFAULT_REQUEST_HEARDERS

    REDIS_MOVIE_DETAIL_URL_KEY = 'movie_spider:detail_urls'

    def start_requests(self):
        start_url = RedisUtil.pop(self.REDIS_MOVIE_DETAIL_URL_KEY)
        if start_url:
            start_url = str(start_url, encoding='utf-8')
            yield scrapy.Request(url=start_url, headers=self.default_headers, callback=self.parse)

    def parse(self, response, **kwargs):
        url = response.url
        try:
            item = TopMovieItem()
            matches = re.findall('\\d+', url)
            item['id'] = int(matches[0])
            item['rate_num'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').extract()[
                    0]
            item['comment_num'] = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()').extract()[0]
            item['five_star_rate'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]/text()').extract()[0]
            item['four_star_rate'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]/text()').extract()[0]
            item['three_star_rate'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]/text()').extract()[0]
            item['two_star_rate'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]/text()').extract()[0]
            item['one_star_rate'] = \
                response.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]/text()').extract()[0]
            yield item
        except IndexError:
            RedisUtil.push(self.REDIS_MOVIE_DETAIL_URL_KEY, url)
        next_url = RedisUtil.pop(self.REDIS_MOVIE_DETAIL_URL_KEY)
        if next_url:
            next_url = str(next_url, encoding='utf-8')
            yield scrapy.Request(url=next_url, headers=self.default_headers, callback=self.parse)
