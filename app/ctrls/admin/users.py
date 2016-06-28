# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_UsersCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        users = self.datum('users').result('select * from users order by user_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if users:
            pager['lgth'] = len(users)

        self.render('admin/users.html', users = users, pager = pager)

class Admin_UserCtrl(AdminCtrl):
    @admin
    def get(self):
        user = self.datum('users').get_user_by_id(self.input('user_id'))
        if not user:
            self.flash(0, {'sta': 404})
            return

        # if user['user_id'] == self.current_user['user_id']:
            # self.flash(0, {'sta': 403})
            # return

        self.render('admin/user.html', user = user)

    @admin
    def post(self):
        user = self.datum('users').get_user_by_id(self.input('user_id'))
        if not user:
            self.flash(0, {'sta': 404})
            return

        if user['user_id'] == self.current_user['user_id']:
            self.flash(0, {'sta': 403})
            return

        try:
            user_mail = self.input('user_mail')
            user_sign = self.input('user_sign')
            user_logo = self.input('user_logo')
            user_meta = self.input('user_meta')
            user_perm = self.input('user_perm')
            user_pswd = self.input('user_pswd', '')
            user_rpwd = self.input('user_rpwd', '')
            user_perm = int(user_perm) & int(self.current_user['user_perm']) & 0x7FFFFFFF

            if user_pswd != user_rpwd:
                self.flash(0, {'msg': '确认密码不匹配'})
                return

            if not self.model('admin').chk_is_user_pswd(user_pswd):
                self.flash(0, {'msg': '无效的用户密码'})
                return

            if not self.model('admin').chk_is_user_mail(user_mail):
                self.flash(0, {'msg': '无效的用户邮箱'})
                return

            if user_mail != user['user_mail'] and self.datum('users').get_user_by_mail(user_mail):
                self.flash(0, {'msg': '用户邮箱已存在'})
                return
            
            if user_pswd:
                user_auid = self.model('admin').generate_randauid()
                user_salt = self.model('admin').generate_randsalt()
                user_pswd = self.model('admin').generate_password(user_pswd, user_salt)
                self.datum('users').affect('update users set user_auid = ?, user_mail = ?, user_sign = ?, user_logo = ?, user_meta, user_pswd = ?, user_salt = ?, user_perm = ?, user_atms = ?, user_utms = ? where user_id = ?',\
                        (user_auid, user_mail, user_sign, user_logo, user_meta, user_pswd, user_salt, user_perm, self.stime(), self.stime(), user['user_id'], ))
            else:
                self.datum('users').affect('update users set user_mail = ?, user_sign = ?, user_logo = ?, user_meta = ?, user_perm = ?, user_utms = ? where user_id = ?',\
                        (user_mail, user_sign, user_logo, user_meta, user_perm, self.stime(), user['user_id'], ))

            self.ualog(self.current_user, "更新用户：" + str(user['user_id']), user['user_name'])
            self.flash(1)
            return
        except:
            pass
        self.flash(0)

class Admin_UserCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/user-create.html')

    @admin
    def post(self):
        try:
            user_name = self.input('user_name')
            user_mail = self.input('user_mail')
            user_perm = self.input('user_perm')
            user_pswd = self.input('user_pswd')
            user_rpwd = self.input('user_rpwd')
            user_sign = self.input('user_sign', '')
            user_logo = self.input('user_logo', '')
            user_meta = self.input('user_meta', '')
            user_ctms = self.stime()
            user_utms = user_ctms
            user_atms = user_ctms

            if len(user_name) < 3 or not self.model('admin').chk_is_user_name(user_name):
                self.flash(0, {'msg': '无效的用户帐号'})
                return
            
            if len(user_pswd) < 6 or (user_pswd != user_rpwd):
                self.flash(0, {'msg': '无效的用户密码'})
                return

            if len(user_mail) < 3 or not self.model('admin').chk_is_user_mail(user_mail):
                self.flash(0, {'msg': '无效的用户邮箱'})
                return

            if self.datum('users').get_user_by_name(user_name):
                self.flash(0, {'msg': '用户帐号已存在'})
                return

            if self.datum('users').get_user_by_mail(user_mail):
                self.flash(0, {'msg': '用户邮箱已存在'})
                return

            user_auid = self.model('admin').generate_randauid()
            user_salt = self.model('admin').generate_randsalt()
            user_pswd = self.model('admin').generate_password(user_rpwd, user_salt)
            user_perm = int(user_perm) & 0x7FFFFFFF

            lastrowid = self.datum('users').affect('insert into users (\
                    user_auid, user_name, user_salt, user_pswd, user_perm, \
                    user_mail, user_sign, user_logo, user_meta, user_ctms, user_utms, user_atms) \
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                    (user_auid, user_name, user_salt, user_pswd, user_perm, user_mail, user_sign, user_logo, user_meta, user_ctms, user_utms, user_atms)).lastrowid
            if lastrowid:
                self.ualog(self.current_user, "新增用户：" + str(lastrowid), user_name)
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
