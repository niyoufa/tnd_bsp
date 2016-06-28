# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_PostsCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        posts = self.datum('posts').result('select * from posts order by post_id desc limit ? offset ?',
                (pager['qnty'], (pager['page']-1)*pager['qnty'], ))

        psers = {}
        if posts:
            pager['lgth'] = len(posts)
            psers = self.utils().array_keyto(self.datum('users').result('select * from users where user_id in (' + ','.join(str(i['user_id']) for i in posts) + ')'), 'user_id')

        self.render('admin/posts.html', pager = pager, posts = posts, psers = psers)

class Admin_PostHiddenCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            post_id = self.input('post_id')

            self.datum('posts').affect('update posts set post_stat = 0 where post_id = ?', (post_id, ))
            self.flash(1)
        except:
            self.flash(0)

class Admin_PostCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        mode = self.input('mode', None)
        terms = self.datum('terms').result('select * from terms order by term_id desc, term_refc desc limit 9')

        self.render('admin/post-create.html', mode = mode, terms = terms)

    @admin
    def post(self):
        try:
            post_title   = self.input('post_title')
            post_descp   = self.input('post_descp')
            post_author  = self.input('post_author')
            post_source  = self.input('post_source')
            post_summary = self.input('post_summary')
            post_content = self.input('post_content')

            post_rank = int(self.input('post_rank'))
            post_stat = int(self.input('post_stat', 0))
            post_ptms = int(self.timer().mktime(self.timer().strptime(self.input('post_ptms'), '%Y-%m-%d %H:%M:%S')))
            post_ctms = self.stime()
            post_utms = post_ctms

            term_list = []
            for term_name in self.input('term_list').split(' '):
                if term_name == '':
                    continue
                term_list.append(term_name)

            if len(term_list) > 10:
                self.flash(0, {'msg': '标签数量限制不能超过 10 个'})
                return

            term_imap = {}
            term_ctms = self.stime()
            for term_name in term_list:
                term_id = self.datum('terms').single('select term_id from terms where term_name = ?', (term_name ,))
                if term_id:
                    term_id = term_id['term_id']
                else:
                    term_id = self.datum('terms').invoke('insert or ignore into terms (term_name, term_ctms) values (?, ?)', (term_name , term_ctms, )).lastrowid
                if term_id:
                    term_imap[term_id] = term_name

            post_id = self.datum('posts').invoke(
                    'insert into posts (user_id, post_title, post_descp, post_author, post_source, post_summary, post_content,post_stat, post_rank, post_ptms, post_ctms, post_utms) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (self.current_user['user_id'], post_title, post_descp, post_author, post_source, post_summary, post_content, post_stat, post_rank, post_ptms, post_ctms, post_utms ,)).lastrowid

            if term_imap:
                for term_id in term_imap:
                    self.datum('posts').invoke('insert or ignore into post_terms (post_id, term_id) values (' + str(post_id) + ',' + str(term_id) + ')')

            if term_imap:
                self.datum('terms').invoke('update terms set term_refc = term_refc + 1 where term_id in (' + ','.join([str(i) for i in term_imap.keys()]) + ')')

            self.datum('posts').commit()
            self.datum('terms').commit()

            self.ualog(self.current_user, '新增文章：' + str(post_id))
            self.flash(1, {'url': '/admin/post?post_id=' + str(post_id)})
        except:
            self.flash(0)


class Admin_PostCtrl(AdminCtrl):
    @admin
    def get(self):
        post_id = self.input('post_id')

        post = self.datum('posts').get_post_by_id(post_id)
        if not post:
            self.flash(0, {'sta': 404})
            return

        mode = self.input('mode', None)

        terms = self.datum('terms').result('select * from terms order by term_id desc, term_refc desc limit 9')
        ptids = self.datum('posts').result('select post_id,term_id from post_terms where post_id = ?', (post_id, ))
        ptags = {}
        if ptids:
            ptags = self.datum('terms').result('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
            if ptags:
                ptids = self.utils().array_group(ptids, 'post_id')
                ptags = self.utils().array_keyto(ptags, 'term_id')

        self.render('admin/post.html', mode = mode, post = post, terms = terms, ptids = ptids, ptags = ptags)

    @admin
    def post(self):
        try:
            post_id      = self.input('post_id')
            post_title   = self.input('post_title')
            post_descp   = self.input('post_descp')
            post_author  = self.input('post_author')
            post_source  = self.input('post_source')
            post_summary = self.input('post_summary')
            post_content = self.input('post_content')

            post_rank = int(self.input('post_rank'))
            post_stat = int(self.input('post_stat', 0))
            post_ptms = int(self.timer().mktime(self.timer().strptime(self.input('post_ptms'), '%Y-%m-%d %H:%M:%S')))
            post_utms = self.stime()

            term_list = []
            for term_name in self.input('term_list').split(' '):
                if term_name == '':
                    continue
                term_list.append(term_name)

            if len(term_list) > 10:
                self.flash(0, {'msg': '标签数量限制不能超过 10 个'})
                return

            post = self.datum('posts').get_post_by_id(post_id)
            if not post:
                self.flash(0, '没有指定文章ID')
                return

            term_imap = {}
            term_ctms = self.stime()
            for term_name in term_list:
                term_id = self.datum('terms').single('select term_id from terms where term_name = ?', (term_name ,))
                if term_id:
                    term_id = term_id['term_id']
                else:
                    term_id = self.datum('terms').invoke('insert or ignore into terms (term_name, term_ctms) values (?, ?)', (term_name , term_ctms, )).lastrowid

                if term_id:
                    term_imap[term_id] = term_name

            post_tids = self.datum('posts').result('select term_id from post_terms where post_id = ?', (post_id, ))

            self.datum('posts').invoke(
                    'update posts set user_id=?,post_title=?,post_descp=?,post_author=?,post_source=?,post_summary=?,post_content=?,post_stat=?,post_rank=?+post_plus-post_mins,post_ptms=?,post_utms=? where post_id=?',
                    (self.current_user['user_id'], post_title, post_descp, post_author, post_source, post_summary, post_content, post_stat, post_rank, post_ptms, post_utms, post_id,))
            self.datum('posts').invoke('delete from post_terms where post_id = ?', (post_id,))

            if term_imap:
                for term_id in term_imap:
                    self.datum('posts').invoke('insert or ignore into post_terms (post_id, term_id) values (' + str(post_id) + ',' + str(term_id) + ')')

            if post_tids:
                self.datum('terms').invoke('update terms set term_refc = term_refc - 1 where term_id in (' + ','.join([str(i['term_id']) for i in post_tids]) + ')')
            if term_imap:
                self.datum('terms').invoke('update terms set term_refc = term_refc + 1 where term_id in (' + ','.join([str(i) for i in term_imap.keys()]) + ')')

            self.datum('posts').commit()
            self.datum('terms').commit()

            self.ualog(self.current_user, '更新文章：' + str(post_id))
            self.flash(1)
        except:
            self.flash(0)
