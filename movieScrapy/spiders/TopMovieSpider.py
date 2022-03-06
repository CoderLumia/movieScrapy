import scrapy
from movieScrapy import settings
from movieScrapy.utils.redisUtils import RedisUtil


class TopMovieSpider(scrapy.Spider):
    name = 'top_movie_spider'

    allow_domain = ['www.douban.com', 'movie.douban.com']

    url_template = 'https://movie.douban.com/top250?start={0}&filter='

    default_headers = settings.DEFAULT_REQUEST_HEARDERS

    REDIS_MOVIE_DETAIL_URL_KEY = 'movie_spider:detail_urls'

    REDIS_TOP_MOVIE_PAGE_KEY = 'movie_spider:top_movie_page_num'

    def start_requests(self):
        yield scrapy.Request(url='https://movie.douban.com/top250?start=0&filter=',
                             headers=self.default_headers,
                             callback=self.parse)

    def parse(self, response, **kwargs):
        start = RedisUtil.get_and_increment(self.REDIS_TOP_MOVIE_PAGE_KEY) * 25
        if start <= 225:
            next_page = self.url_template.format(start)
            ol = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
            for li in ol:
                detail_urls = li.xpath('div/div[1]/a/@href').extract()
                if len(detail_urls) > 0:
                    RedisUtil.push(self.REDIS_MOVIE_DETAIL_URL_KEY, detail_urls[0])
            yield scrapy.Request(url=next_page,headers=self.default_headers,callback=self.parse)
