# -*- coding:utf-8 -*-
import time
import traceback
from functools import wraps


class TimeUtil(object):
    DATE_FORMAT = "%Y.%m.%d"

    @staticmethod
    def parse_date_to_timestamp(date_str, date_format=DATE_FORMAT):
        return time.mktime(time.strptime(date_str, date_format))


def exception_handler(the_func):
    @wraps(the_func)
    def wrap_the_function(*args, **kwargs):
        try:
            return the_func(*args, **kwargs)
        except Exception, e:
            # print e
            traceback.print_exc()
            return unicode(e)

    return wrap_the_function
