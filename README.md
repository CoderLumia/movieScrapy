- # movieScrapy

### 豆瓣电影数据分析
#### 一、爬取豆瓣电影

- douban_movie 豆瓣电影全量数据

- top_movie_item 豆瓣电影TOP250数据

#### 二、电影指标

- 豆瓣电影TOP10

- 发行地区数量分布

- 电影数量增长趋势

- 最受欢迎演员TOP10

- 最受欢迎导员TOP10

- 豆瓣评分分布

- 电影时长分布

- 豆瓣电影TOP250电影类型分布

- 豆瓣电影TOP250评价占比

#### 三、爬取数据

首先，使用Scrapy创建爬虫项目scrapy startproject  movieScrapy

在spider包下是所有的爬虫代码，`MovieSpider`爬取所有电影数据，`TopMovieSpider`爬取豆瓣电影Top250列目，`TopMovieItemSpider`爬取电影详情数据。

在pipelines中将爬取的数据详情写入到数据库中。

在settings中，配置请求头，数据库连接配置等参数

```python
faker = Factory.create(locale='zh_CN')

DEFAULT_REQUEST_HEARDERS = {
    'Host': 'movie.douban.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'User_Agent': faker.user_agent()
}

REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0
}

MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'movie_scrapy',
    'charset': 'utf8'
}
```

爬虫启动方式：

- scrapy crawl movie_spider 爬取全量电影数据
- scrapy crawl top_movie_spider 爬取电影详情url
- scrapy crawl top_movie_item_spider 爬取电影详情数据

#### 四、数据分析

1. 将mysql数据库中的数据集成到阿里云平台上的maxcompute中
2. 根据数据分析指标在maxcompute上编写sql语句
3. 将分析指标查询结果同步回mysql
4. 使用FineBI软件中同步mysql中指标数据
5. 在FineBI中根据相应指标创建仪表板



