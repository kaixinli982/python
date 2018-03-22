# -*- coding: UTF-8 -*-
import logging

def checkprint(succeed="成功", faild="失败"):
    def check_init(func):
        def check(self, dothing, *args, **kargs):
            if func(self, dothing, *args, **kargs):
                logging.info(str(dothing) + succeed)
                return True
            else:
                logging.info(str(dothing) + faild)
                return False
        return check
    return check_init