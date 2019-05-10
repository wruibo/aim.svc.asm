"""
    spider manager
"""
import threading
import tornado.ioloop, tornado.log
from . import error


class _SpiderManager(threading.Thread):
    def __init__(self):
        """
            init spider manager
        """
        # registered spiders, id->spider
        self._spiders = {}
        # tornado non-blocking io event loop
        self._ioloop = tornado.ioloop.IOLoop.current()

        super().__init__(name='spider manager')

    def register(self, spider):
        """
            register a spider
        :param spider: object, spider instance
        :return:
        """
        self._spiders[spider.id] = spider

    def enable(self, spider=None):
        """
            enable a spider
        :param spider: str, spider id
        :return:
        """
        if spider is None:
            for spider in self._spiders.values():
                spider.enable()
        else:
            if self._spiders.get(spider) is not None:
                self._spiders[spider].enable()

    def disable(self, spider=None):
        """
            disable a spider
        :param spider: str, spider id
        :return:
        """
        if spider is None:
            for spider in self._spiders.values():
                spider.disable()
        else:
            if self._spiders.get(spider) is not None:
                self._spiders[spider].disable()

    def status(self, spider=None):
        """
            get spider status
        :param spider: str, spider id
        :return:
        """
        if spider is None:
            result = []
            for spider in self._spiders.values():
                result.append(spider.status())
        else:
            if self._spiders.get(spider) is not None:
                result = self._spiders[spider].status()
            else:
                raise error.SpiderError('spider %s not exist' % str(spider))
        return result

    async def _schedule(self):
        """
            schedule spiders
        :return:
        """
        for id, spider in self._spiders.items():
            if spider.timeup() and not spider.running and not spider.disabled:
                await spider.execute()
        self._ioloop.call_later(1.0, self._schedule)

    def run(self):
        """
            run io event loop
        :return:
        """
        self._ioloop.call_later(1.0, self._schedule)
        # run for every
        #self._ioloop.start()


_default_spider_manager = _SpiderManager()


def register(spider):
    """
        register a spider to manager
    :param spider: object, instance of Spider
    :return:
    """
    _default_spider_manager.register(spider)


def start():
    _default_spider_manager.enable()
    _default_spider_manager.start()


def enable(spider=None):
    _default_spider_manager.enable(spider)


def disable(spider=None):
    _default_spider_manager.disable(spider)


def status(spider=None):
    return _default_spider_manager.status(spider)
