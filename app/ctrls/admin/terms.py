# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_TermsCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        terms = self.datum('terms').result(
                'select * from terms order by term_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if terms:
            pager['lgth'] = len(terms)

        self.render('admin/terms.html', terms = terms, pager = pager)

class Admin_TermCtrl(AdminCtrl):
    @admin
    def get(self):
        term_id = self.input('term_id')
        term = self.datum('terms').single('select * from terms where term_id = ?', (term_id,))
        if not term:
            self.flash(0, {'sta': 404})
            return

        self.render('admin/term.html', entry = term)

    @admin
    def post(self):
        try:
            term_id   = self.input('term_id')
            term_name = self.input('term_name')

            if self.datum('terms').affect('update terms set term_name = ? where term_id = ?',
                    (term_name, term_id ,)).rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_TermCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/term-create.html')

    @admin
    def post(self):
        try:
            term_name = self.input('term_name')
            term_ctms = self.stime()

            if self.datum('terms').affect('insert into terms (term_name, term_ctms) values (?, ?)', (term_name, term_ctms ,)).lastrowid:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
