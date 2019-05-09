"""
    store for news
"""
from . import util
from .. import models
import tornado.log


def distinct(site, items, idextractor=None):
    """
        get distinct source news items from input which not exist in store identified by site and item id
    :param site: str, source site
    :param items: array, source news item list
    :param idextractor: function, extract source id from item
    :return:
        array, news items not exist in store
    """
    sids = [idextractor(item) for item in items]
    sql = 'select sid from tb_news where site=%s and sid in (' +','.join(['%s' for i in range(0, len(sids))])+ ')'
    with models.db.create() as d:
        exists = models.model.RawModel.select(d, sql, site, *sids)
        newsids = set(sids) - set([item['sid'] for item in exists])

        newitems = []
        for item in items:
            if idextractor(item) in newsids:
                newitems.append(item)
        return newitems


def insert(*items):
    """
        insert new items to store
    :param items: array, news items to be inserted, item:
            {
                'category_id': category,
                'title': title,
                'brief': description,
                'body': body,
                'images': images, split by ','
                'tags': tags, split by ',',
                'source': source,
                'site': site,
                'sid': news id in site,
                'disabled': False,
                'ptime': publish time,
                'ctime': create time,
                'mtime': modify time
            }
    :return:
    """
    with models.db.atomic() as d:
        for item in items:
            if item['brief'] is None or str(item['brief']).strip()=='':
                item['brief'] = item['title']
            models.News(code=util.uuid(), **item).save(d)
            tornado.log.app_log.info('news-insert: %s', item['title'])
