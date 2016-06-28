# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_TalksCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        talks = self.datum('talks').result('select * from talks order by talk_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if talks:
            pager['lgth'] = len(talks)

        self.render('admin/talks.html', pager = pager, talks = talks)

class Admin_TalkCtrl(AdminCtrl):
    @admin
    def get(self):
        talk_id = self.input('talk_id')
        talk = self.datum('talks').single('select * from talks where talk_id = ?', (talk_id ,))
        if not talk:
            self.flash(0, {'sta': 404})
            return

        self.render('admin/talk.html', talk = talk)

    @admin
    def post(self):
        try:
            talk_id   = self.input('talk_id')
            user_name = self.input('user_name')
            user_mail = self.input('user_mail')
            talk_rank = self.input('talk_rank')
            talk_text = self.input('talk_text')
            talk_utms = self.stime()

            if self.datum('talks').affect(
                    'update talks set user_name = ?, user_mail = ?, talk_rank = ?+talk_plus-talk_mins, talk_text = ?, talk_utms = ? where talk_id = ?',
                    (user_name, user_mail, talk_rank, talk_text, talk_utms, talk_id ,)).rowcount:
                self.ualog(self.current_user, '更新评论：' + str(talk_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_TalkDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            talk_id   = self.input('talk_id')
            talk_ctms = self.input('talk_ctms')

            if self.datum('talks').affect(
                    'delete from talks where talk_id = ? and talk_ctms = ?', (talk_id, talk_ctms ,)).rowcount:
                self.ualog(self.current_user, '删除评论：' + str(talk_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
