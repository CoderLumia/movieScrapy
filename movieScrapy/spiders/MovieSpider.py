import scrapy
import json
from movieScrapy.items import MovieItem
from movieScrapy.utils.redisUtils import RedisUtil
from movieScrapy.settings import DEFAULT_REQUEST_HEARDERS


class MovieSpider(scrapy.Spider):
    name = 'movie_spider'
    allowed_domain = ['douban.com']
    start_urls = [
        'https://movie.douban.com/j/new_search_subjects?sort=U&start=0']

    headers = DEFAULT_REQUEST_HEARDERS

    PAGE_NUM_KEY = "movie_spider:page_num"

    custom_settings = {
        'ITEM_PIPELINES': {'movieScrapy.pipelines.MoviesPipeline': 300}
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&start=0'

        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    # 获取汇总数据
    def parse(self, response, **kwargs):
        page_num = RedisUtil.get_and_increment(self.PAGE_NUM_KEY)
        response_data = json.loads(response.body)
        if 'data' in response_data and len(response_data['data']) > 0:
            subjects = response_data['data']
            for subject in subjects:
                movie_item = MovieItem()
                movie_item['id'] = subject['id']
                movie_item['url'] = subject['url']
                movie_item['title'] = subject['title']
                movie_item['rate'] = subject['rate']
                movie_item['cover'] = subject['cover']
                movie_item['is_new'] = 0
                subject_url = 'https://movie.douban.com/j/subject_abstract?subject_id=' + subject['id']
                yield scrapy.Request(url=subject_url, callback=self.parse_getSubject, meta={'movie_item': movie_item},
                                     headers=self.headers)
            url = 'https://movie.douban.com/j/new_search_subjects?sort=U&start={0}'.format(page_num * 20)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    # 获取详情数据
    def parse_getSubject(self, response):
        response_data = json.loads(response.body)
        if 'subject' in response_data:
            subject = response_data['subject']
            movie_item = response.meta['movie_item']
            movie_item['short_comment'] = subject['short_comment']['content'] if 'content' in subject[
                'short_comment'].keys() else ''
            movie_item['directors'] = ';'.join(subject['directors'])
            movie_item['actors'] = ';'.join(subject['actors'])
            movie_item['duration'] = subject['duration']
            movie_item['region'] = subject['region']
            movie_item['types'] = ';'.join(subject['types'])
            movie_item['release_year'] = subject['release_year']
            yield movie_item
