"""
    time counter for timer
"""
import time, datetime


class Cron:
    def timeup(self):
        pass


class Interval(Cron):
    def __init__(self, seconds):
        """
            init interval timer
        :param seconds:
        """
        self._interval = seconds
        self._last = int(time.time())

    def __str__(self):
        return "Interval(%s)" % self._interval

    def timeup(self):
        """
            check time up of interval
        :return:
        """
        # check now with last time up timestamp
        now = int(time.time())
        if now - self._last < self._interval:
            return False
        # reset last time up pint
        self._last = now
        # time up
        return True


class TimePoint(Cron):
    def __init__(self, min=None, hour=None, day=None, month=None, week=None, year=None):
        """
            init time point timer
        :param min: int, 0~59
        :param hour: int, 0~23
        :param day: int, 1~31
        :param month: int, 1~12
        :param week: int, 1~7
        :param year: int, 0~....
        """
        # time point conditions
        self._min = min
        self._hour = hour
        self._day = day
        self._month = month
        self._week = week
        self._year = year

        # last time up datetime
        self._last = None

    def __str__(self):
        return 'TimePoint(min:%s, hour:%s, day:%s, month:%s, week:%s, year:%s)' % (self._min, self._hour, self._day, self._month, self._week, self._year)

    def timeup(self):
        """
            check time up of time point
        :return:
        """
        # current datetime
        now = datetime.datetime.now()

        # check last time up point
        if self._last is not None:
            delta = now - self._last
            if delta.days==0 and delta.seconds<60: # already triggered
                return False

        # check if time up
        if (self._min is not None and self._min != now.min) \
            or (self._hour is not None and self._hour != now.hour) \
            or (self._day is not None and self._day != now.day) \
            or (self._month is not None and self._month != now.month) \
            or (self._week is not None and self._week != now.isoweekday()) \
            or (self._year is not None and self._year != now.year):
            return False

        # reset last time up point
        self._last = now
        # time up
        return True
