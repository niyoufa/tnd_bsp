# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_IndexCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        talks = self.datum('talks').result('select * from talks order by talk_id desc limit 3')
        mails = self.datum('mails').result('select * from mails order by mail_id desc limit 3')
        self.render('admin/index.html', talks = talks, mails = mails)
