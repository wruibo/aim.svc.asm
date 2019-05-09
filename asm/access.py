"""
    access protection
"""
import tornado.web, logging, traceback
from . import error, protocol


def protect(handler_func):
    def wrapper(self, *args, **kwargs):
        try:
            return handler_func(self, *args, **kwargs)
        except tornado.web.MissingArgumentError as e:
            self.write(protocol.failed(msg=str(error.USER_PARAM_INVALID)))
            logging.error(traceback.format_exc())
        except error.UserError as e:
            self.write(protocol.failed(msg=str(e)))
            logging.error(traceback.format_exc())
        except Exception as e:
            self.write(protocol.failed(msg=str(error.SYSTEM_ERROR)))
            logging.error(traceback.format_exc())
    return wrapper
