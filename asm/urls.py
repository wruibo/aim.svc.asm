from . import handlers

handlers = [
    (r"/enable", handlers.spider.EnableHandler),
    (r"/disable", handlers.spider.DisableHandler),
    (r"/status", handlers.spider.StatusHandler),
]
