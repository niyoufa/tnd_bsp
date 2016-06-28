# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class ApplyCtrl(BasicCtrl):
    def get(self):
        self.redirect("/about#email")
