# -*- coding: UTF-8 -*-

from basic import login, BasicCtrl

class LeaveCtrl(BasicCtrl):
    @login
    def get(self):
        self.render('leave.html')

    @login
    def post(self):
        self.del_current_sess()
        self.redirect('/')
