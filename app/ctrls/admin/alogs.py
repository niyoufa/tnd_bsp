# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_AlogsCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        alogs = self.datum('alogs').result(
                'select * from alogs order by alog_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))

        if alogs:
            pager['lgth'] = len(alogs)

        self.render('admin/alogs.html', alogs = alogs, pager = pager)
