"""
    news spider for east money
"""
import re, time, datetime, tornado.log
from . import config
from .. import spider, manager, timer, util
from ... import stores


class _NewsListFetcher:
    """
        get news items list by category id
    """
    URL = 'http://m.eastmoney.com/newslist/GetNewsListData?columnid=%s&thispage=1'

    def __init__(self, category):
        self.category = category
        self.fetcher = spider.Item(self.URL % category.id, category.interval)

    async def fetch(self):
        """

        :return:
        """
        try:
            response = await self.fetcher.fetch()
            if response is not None and response.code == 200:
                content = response.body.decode()
                items = util.json(content)
                return items
        except Exception as e:
            tornado.log.app_log.error('fetch news list of category: %s, error: %s', self.category.name, str(e))


class _DetailFetcher:
    """
        get news detail by news id
    """
    # detail url
    URL = 'http://newsinfo.eastmoney.com/kuaixun/v2/api/content/getnews?newsid=%s&newstype=1&callback=json'

    def __init__(self, id):
        self._id = id
        self._url = self.URL % id

    async def fetch(self):
        """

        :return:
        """
        try:
            response = await spider.fetch(self._url)
            if response is not None and response.code == 200:
                # get content
                content = response.body.decode()
                #parse content
                detail = util.json(content, '(', ')')['news']
                return detail
        except Exception as e:
            tornado.log.app_log.error('fetch news detail of code: %s, error: %s', self._id, str(e))


class _DetailParser:
    """
        parse normalized news express item from fetched detail
    """
    def __init__(self, category, item, detail):
        """
            parse detail to normalized news express item
        :param category: object, configure category object
        :param item: dict, item of site news list
        :param detail: dict, detail of news content
        """
        self._category = category
        self._item = item
        self._detail = detail

    @staticmethod
    def empty(s):
        if s is None or s=='' or s=='null':
            return True
        return False

    def body(self):
        elements = re.split(r'(<!--[\s\w_#]+-->)', self._detail['body'])
        for i in range(0, len(elements)):
            mobj = re.match(r'<!--(Link|IMG)#(\d+)-->', elements[i])
            if not mobj:
                if re.match(r'(<!--.*-->)', elements[i]):
                    elements[i] = ''
                continue

            type, index = mobj[1], mobj[2]
            if type == 'Link':
                elements[i] = self.link(index)
            elif type == 'IMG':
                elements[i] = self.img(index)
            else:
                pass
        return ''.join(elements)

    def link(self, index):
        item = self._detail['links'][int(index)]
        # only keep the text
        return item['text']

    def img(self, index):
        item = self._detail['images'][int(index)]
        results = ['<img']
        # attributes
        if not self.empty(item.get('src')):
            results.append(' src="%s"'%item['src'])
        if not self.empty(item.get('border')):
            results.append(' border="%s"'%item['border'])
        if not self.empty(item.get('style')):
            results.append(' style="%s"'%item['style'])
        if not self.empty(item.get('width')):
            results.append(' width="%s"' % item['width'])
        if not self.empty(item.get('height')):
            results.append(' height="%s"' % item['height'])

        results.append('>')

        return ''.join(results)

    def images(self):
        return self._detail['smallimage']

    def tags(self):
        return self._category.name

    def ptime(self):
        return datetime.datetime.strptime(self._detail['showtime'], '%Y-%m-%d %H:%M:%S').timestamp()

    def parse(self):
        try:
            if isinstance(self._detail, dict):
                return {
                    'category_id': self._category.category,
                    'title': self._detail['title'],
                    'brief': self._detail['description'],
                    'body': self.body(),
                    'images': self.images(),
                    'tags': self.tags(),
                    'source': self._detail['source'],
                    'site': config.SITE,
                    'sid': self._detail['newsid'],
                    'disabled': False,
                    'ptime': self.ptime(),
                    'ctime': time.time(),
                    'mtime': time.time()
                }
        except Exception as e:
            tornado.log.app_log.error('parse news detail error: %s', str(e))


# 新闻
class DfcfNewsSpider(spider.Spider):
    # news list url for page 1
    def __init__(self, id, name, cron):
        """
            init spider
        :param id:
        :param name:
        :param cron:
        """
        self._fetchers = [_NewsListFetcher(category) for category in config.news.categories]
        super().__init__(id, name, cron)

    async def run(self):
        """
            execute spider once
        :return:
            running result
        """
        try:
            category_total, category_updated, news_total, news_updated = len(self._fetchers), 0, 0, 0
            # process each news category
            for fetcher in self._fetchers:
                # fetch first page news list of current category
                items = await fetcher.fetch()
                # process news items of first page
                if items is not None:
                    category_updated += 1
                    news_total += len(items)
                    # filter not exist news ids
                    items = stores.news.distinct(config.SITE, items, lambda item: item['Code'])

                    # process each news item detail
                    newitems = []
                    for item in items:
                        # fetch news detail data
                        detail = await _DetailFetcher(item['Code']).fetch()
                        if detail is not None:
                            newitem = _DetailParser(fetcher.category, item, detail).parse()
                            if newitem is not None:
                                newitems.append(newitem)
                    # save to news store
                    stores.news.insert(*newitems)
                    news_updated += len(newitems)
            tornado.log.app_log.info('spider-%s-news: category(total: %s, updated: %s), news(total: %s, updated: %s)', config.SITE, category_total, category_updated, news_total, news_updated)
        except Exception as e:
            tornado.log.app_log.error('spider-%s-news: %s', config.SITE, str(e))


# register spider to manager
manager.register(DfcfNewsSpider('dfcf.news', '东方财富新闻', timer.Interval(5)))


