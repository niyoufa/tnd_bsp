# -*- coding: UTF-8 -*-

import functools

from app.ctrls.basic import alive, BasicCtrl

class ShellCtrl(BasicCtrl):
    pass

def shell(method):
    @alive
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(self, *args, **kwargs)
    return wrapper

