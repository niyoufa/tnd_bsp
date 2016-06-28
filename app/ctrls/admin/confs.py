# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_ConfsCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        confs = self.datum('confs').result(
                'select * from confs order by conf_ctms desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))

        if confs:
            pager['lgth'] = len(confs)

        self.render('admin/confs.html', pager = pager, confs = confs)

class Admin_ConfCtrl(AdminCtrl):
    @admin
    def get(self):
        conf_name = self.input('conf_name')
        conf = self.datum('confs').single('select * from confs where conf_name = ? limit 1', (conf_name, ))
        if not conf:
            self.flash(0, {'sta': 404})
            return

        self.render('admin/conf.html', entry = conf)

    @admin
    def post(self):
        try:
            conf_name = self.input('conf_name')
            conf_vals = self.input('conf_vals')

            self.datum('confs').upsert(conf_name, conf_vals)

            self.ualog(self.current_user, "更新配置：" + conf_name, conf_vals)
            self.flash(1, {'msg': '更新配置成功'})
        except:
            self.flash(0)

class Admin_ConfCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/conf-create.html')

    @admin
    def post(self):
        try:
            conf_name = self.input('conf_name')
            conf_vals = self.input('conf_vals')

            if len(conf_name) > 32:
                self.flash(0, {'msg': '配置键长度不能超过32个字符'})
                return

            if self.datum('confs').exists(conf_name):
                self.flash(0, {'msg': '配置键已存在'})
                return

            self.datum('confs').upsert(conf_name, conf_vals)

            self.ualog(self.current_user, "新增配置：" + conf_name, conf_vals)
            self.flash(1, {'msg': '新增配置成功'})
        except:
            self.flash(0)

class Admin_ConfDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            conf_name = self.input('conf_name')
            conf_vals = self.get_runtime_conf(conf_name)

            self.datum('confs').delete(conf_name)

            self.ualog(self.current_user, "删除配置：" + conf_name, conf_vals)
            self.flash(1, {'msg': '删除配置成功'})
        except:
            self.flash(0)
