# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class LinksCtrl(BasicCtrl):
    def get(self):
        links = self.datum('links').result(
                'select * from links where link_rank>0 order by link_rank desc, link_id desc')

        self.render('links.html', links = links)
