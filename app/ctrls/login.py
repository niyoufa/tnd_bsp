# -*- coding: UTF-8 -*-

from basic import BasicCtrl
import pdb

class LoginCtrl(BasicCtrl):
    def get(self):
        self.render('login.html', next = self.input('next', '/shell'))

    def post(self):
        pdb.set_trace()
        if not self.human_valid():
            self.flash(0, {'msg': '验证码错误'})
            return

        try:
            username = self.input('username')
            password = self.input('password')
            remember = self.input('remember', None)
            redirect = self.input('redirect', '/shell')

            if remember:
                remember = int(remember)

            user = self.datum('users').get_user_by_name(username)

            if user and self.entry('login:user#' + str(user['user_id'])):
                self.flash(0, {'msg': '操作太频繁，请稍后再试', 'sta': 429})
                return

            if user and self.model('admin').generate_password(password, user['user_salt']) == user['user_pswd']:
                self.set_current_sess(user, days = remember)

                self.ualog(user, '登陆')
                self.flash(1, {'url': redirect})
                return
        except:
            pass

        self.flash(0, {'msg': '用户名或密码错误'})
