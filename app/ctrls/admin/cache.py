# -*- coding: UTF-8 -*-

import re
from . import admin, AdminCtrl

class Admin_CacheCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/cache.html')

class Admin_CacheDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            self.cache().delete(self.input('exp'), exp = True)
            self.flash(1)
        except:
            self.flash(0)
