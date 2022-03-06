# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re
from movieScrapy.utils.mysqlUtils import MysqlUtils


class MoviesPipeline:

    def process_item(self, item, spider):
        item = self.transform_item(item)
        if item:
            self.upsert_movie_item(item)
        return item

    # 清洗数据格式
    @classmethod
    def transform_item(cls, item):
        if item['id']:
            item['id'] = int(item['id'])
        else:
            return None
        if item['is_new']:
            item['is_new'] = 1
        else:
            item['is_new'] = 0
        if len(item['duration'].strip()) > 0:
            duration = item['duration']
            item['duration'] = int(duration[0:duration.rfind('分', 1)])
        else:
            return None
        if item['rate']:
            item['rate'] = int(float(item['rate']) * 10)
        else:
            return None
        return item

    @classmethod
    def upsert_movie_item(cls, item):
        sql = 'replace into douban_movie(id, title, url, cover, rate, is_new, ' \
              'short_comment, directors, actors, duration, region, types, release_year, create_time, update_time) ' \
              'values({id}, \'{title}\', \'{url}\', \'{cover}\', {rate}, \'{is_new}\',' \
              ' \'{short_comment}\', \'{directors}\',' \
              ' \'{actors}\', {duration}, \'{region}\', \'{types}\', \'{release_year}\', now(), now()) '
        exec_sql = sql.format_map(item)
        MysqlUtils.upsert(exec_sql)


class TopMoviePipeLine:

    @classmethod
    def process_item(cls, item, spider):
        item = cls.transform_item(item)
        if item:
            cls.upsert_top_movie(item)

    @classmethod
    def upsert_top_movie(cls, item):
        sql = 'replace into top_movie_item(id, rate_num, comment_num, five_star_rate, four_star_rate, three_star_rate, two_star_rate, one_star_rate)' \
              'values({id}, {rate_num}, {comment_num}, {five_star_rate}, {four_star_rate}, {three_star_rate}, {two_star_rate}, {one_star_rate})'
        exec_sql = sql.format_map(item)
        MysqlUtils.upsert(exec_sql)

    @classmethod
    def transform_item(cls, item):
        if item['id']:
            item['id'] = int(item['id'])
        else:
            return None
        if item['rate_num']:
            item['rate_num'] = int(item['rate_num'])
        else:
            return None
        if item['comment_num']:
            matches = re.findall('\\d+', item['comment_num'])
            if len(matches) > 0:
                item['comment_num'] = int(matches[0])
            else:
                item['comment_num'] = 0
        else:
            return None
        for key in item:
            if str(key).endswith('_star_rate'):
                if len(item[key]) > 0:
                    rate = item[key]
                    item[key] = float(rate[0:rate.rfind('%', 1)]) * 10
                else:
                    item[key] = 0
        return item
