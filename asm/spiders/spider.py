"""
    spider base class
"""
import time
from tornado import httpclient
from . import timer


async def fetch(url):
    return await httpclient.AsyncHTTPClient().fetch((url))


class Spider:
    """
        spider which implements an independent spider task
    """
    def __init__(self, id, name, cron):
        """
            init spider with cron profile
        :param id: str, spider unique id
        :param name: str, spider name
        :param cron: object, Interval or TimePoint
        """
        self._id = id
        self._name = name
        self._cron = cron

        self._disabled = False
        self._is_running = False

        self._counter = 0
        self._last_start_time = None
        self._last_finish_time = None
        self._last_execute_result = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def running(self):
        """
            is running
        :return:
        """
        return self._is_running

    @property
    def disabled(self):
        return self._disabled

    def enable(self):
        """
            enable spider
        :return:
        """
        self._disabled = False

    def disable(self):
        """
            disable spider
        :return:
        """
        self._disabled = True

    def status(self):
        """
            get spider status
        :return:
        """
        return {
            'id': self._id,
            'name': self._name,
            'cron': str(self._cron),
            'disabled': self._disabled,
            'running': self._is_running,
            'count': self._counter,
            'lstime': self._last_start_time,
            'lftime': self._last_finish_time,
            'lresult': self._last_execute_result
        }

    def timeup(self):
        """
            check time up for spider to execute
        :return:
        """
        return self._cron.timeup()

    async def fetch(self, url):
        """
            fetch a url async
        :param url:
        :return:
        """
        return await fetch(url)

    async def execute(self):
        # update status
        self._is_running = True
        self._last_start_time = int(time.time())
        self._last_finish_time = None
        self._last_execute_result = None
        self._counter += 1

        # execute spider
        result = await self.run()

        # update status
        self._is_running = False
        self._last_execute_result = result
        self._last_finish_time = int(time.time())

        return result

    async def run(self):
        """
            subclass must be implements this method
        :return:
        """
        raise NotImplementedError()


class Item:
    """
        spider item with time up interval which implements an url spider task
    """
    def __init__(self, url, interval):
        """

        :param url:
        :param interval:
        """
        self._url = url
        self._cron = timer.Interval(interval)

    async def fetch(self):
        if not self._cron.timeup():
            return None
        return await fetch(self._url)