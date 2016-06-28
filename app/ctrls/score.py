# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class ScoreCtrl(BasicCtrl):
    def post(self):
        try:
            self.datum('posts').affect(
                    'update posts set post_rank = post_rank + 1, post_plus = post_plus + 1 where post_id = ? limit 1', (self.input('poid'),))
            self.flash(1)
        except:
            self.flash(0)
