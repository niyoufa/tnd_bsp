# -*- coding: UTF-8 -*-

from . import shell, ShellCtrl

class Shell_IndexCtrl(ShellCtrl):
    def get(self, name):
        stime = self.stime()
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        user = self.datum('users').get_user_by_name(name)
        if not user:
            self.flash(0, {'sta': 404})
            return

        posts = self.datum('posts').result(
                'select * from posts where user_id=? and post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?',
                (user['user_id'], stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))

        if posts:
            pager['lgth'] = len(posts)

        if self.input('_pjax', None) == '#shell-index-posts':
            self.render('shell/index/posts.html', user = user, pager = pager, posts = posts)
            return

        self.render('shell/index.html', user = user, pager = pager, posts = posts)
