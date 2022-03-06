# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # 豆瓣电影主键
    url = scrapy.Field()  # 详情url
    title = scrapy.Field()  # 电影名称
    rate = scrapy.Field()  # 豆瓣评级
    cover = scrapy.Field()  # 封面url
    is_new = scrapy.Field()  # 是否为新电影
    short_comment = scrapy.Field()  # 评论
    directors = scrapy.Field()  # 导演
    actors = scrapy.Field()  # 演员
    duration = scrapy.Field()  # 时长
    region = scrapy.Field()  # 地区
    types = scrapy.Field()  # 电影类型
    release_year = scrapy.Field()  # 发行年份
    pass


# 豆瓣电影Top250
class TopMovieItem(scrapy.Item):
    id = scrapy.Field()
    rate_num = scrapy.Field()
    comment_num = scrapy.Field()
    five_star_rate = scrapy.Field()
    four_star_rate = scrapy.Field()
    three_star_rate = scrapy.Field()
    two_star_rate = scrapy.Field()
    one_star_rate = scrapy.Field()
    pass
