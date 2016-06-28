# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_LinksCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        links = self.datum('links').result(
                'select * from links order by link_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if links: 
            pager['lgth'] = len(links)

        self.render('admin/links.html', pager = pager, links = links)

class Admin_LinkCtrl(AdminCtrl):
    @admin
    def get(self):
        link_id = self.input('link_id')
        link = self.datum('links').single('select * from links where link_id = ?', (link_id,))
        if not link:
            self.flash(0, {'sta': 404})
            return

        self.render('admin/link.html', entry = link)

    @admin
    def post(self):
        try:
            link_id   = self.input('link_id')
            link_name = self.input('link_name')
            link_href = self.input('link_href')
            link_desp = self.input('link_desp')
            link_rank = self.input('link_rank')
            link_utms = self.stime()

            if self.datum('links').affect(
                    'update links set link_name = ?, link_href = ?, link_desp = ?, link_rank = ?, link_utms = ? where link_id = ?',
                    (link_name, link_href, link_desp, link_rank, link_utms, link_id ,)).rowcount:
                self.ualog(self.current_user, '更新链接：' + str(link_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_LinkCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/link-create.html')

    @admin
    def post(self):
        try:
            link_name = self.input('link_name')
            link_href = self.input('link_href')
            link_desp = self.input('link_desp')
            link_rank = self.input('link_rank')
            link_ctms = self.stime()
            link_utms = link_ctms

            lastrowid = self.datum('links').affect(
                    'insert into links (link_name, link_href, link_desp, link_rank, link_ctms, link_utms) values (?, ?, ?, ?, ?, ?)',
                    (link_name, link_href, link_desp, link_rank, link_ctms, link_utms ,)).lastrowid
            if lastrowid:
                self.ualog(self.current_user, "新增链接：" + str(lastrowid), link_href)
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_LinkDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            link_id   = self.input('link_id')
            link_utms = self.input('link_utms')

            if self.datum('links').affect(
                    'delete from links where link_id = ? and link_utms = ?', (link_id, link_utms ,)).rowcount:
                self.ualog(self.current_user, '删除链接：' + str(link_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
