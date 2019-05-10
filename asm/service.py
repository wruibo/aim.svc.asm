"""
    service
"""
import tornado.ioloop, tornado.web, tornado.options, tornado.log, logging

from asm import config, urls, models, spiders

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# setup service
def setup(mode):
    """
        setup service environments
    :param mode: str, dev/test/online
    :return:
    """
    # setup database
    models.setup(mode)


# start asm service
def start():
    # set command options
    tornado.options.define('mode', default='dev', help='service mode(dev|test|online), default dev', type=str)
    tornado.options.define('port', default=9005, help='service port', type=int)
    tornado.options.parse_command_line()

    # setup service
    setup(tornado.options.options.mode)

    # start spider service
    spiders.manager.start()

    # service port
    port = tornado.options.options.port

    # log format
    formatter = tornado.log.LogFormatter(fmt='%(color)s[%(asctime)s][%(name)s][%(levelname)s]%(end_color)s %(message)s [%(filename)s, %(lineno)d]', datefmt='%Y/%m/%d %H:%M:%S', color=False)
    for logger in logging.getLogger().handlers:
        logger.setFormatter(formatter)

    # log start message
    tornado.log.gen_log.info('start asm service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    """
        python3 service.py --mode=dev --port=9005 --log_file_prefix='../asm.9005.log' --log_rotate_mode='time' --log_rotate_when='D' --log_rotate_interval=1 
    """
    start()
