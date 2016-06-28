# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class EmailCtrl(BasicCtrl):
    def post(self):
        if not self.human_valid():
            self.flash(0, {'msg': '验证码错误'})
            return

        name = self.input('name')
        mail = self.input('mail')
        text = self.input('text')
        time = self.stime()

        if self.datum('mails').affect(
                'insert into mails (user_ip, user_name, user_mail, mail_text, mail_ctms, mail_utms) values (?, ?, ?, ?, ?, ?)',
                (self.request.remote_ip, name, mail, text, time, time)).lastrowid:
            self.flash(1)
            self.email('%s <%s>' %(name, mail), self.jsons(self.get_runtime_conf('mails')),
                    'Received Feedback (%s)' % self.timer().strftime('%F %T %Z', self.timer().localtime(time)),
                    'Mail From %s <%s>:\r\n\r\n%s' %(name, mail, text))
        else:
            self.flash(0)
