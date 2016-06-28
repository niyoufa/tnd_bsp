# -*- coding: UTF-8 -*-

import os, re, sys, hashlib, mimetypes
from . import admin, AdminCtrl

class Admin_FilesCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        files = self.datum('files').result(
                'select * from files order by file_id desc limit ? offset ?',
                (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if files:
            pager['lgth'] = len(files)

        self.render('admin/files.html', pager = pager, files = files)

class Admin_FileCtrl(AdminCtrl):
    @admin
    def get(self):
        self.flash(0)

class Admin_FileUploadCtrl(AdminCtrl):
    def check_xsrf_cookie(self):
        return True

    @admin
    def get(self):
        self.render('admin/file-upload.html')

    @admin
    def post(self):
        if 'upload' not in self.request.files or len(self.request.files['upload']) < 1:
            self.flash(0, {'msg': '没有上传文件'})
            return

        res = self.request.files['upload'][0]

        if 'content_type' not in res or res['content_type'].find('/') < 1 or len(res['content_type']) > 128:
            self.flash(0, {'msg': '文件类型错误'})
            return

        if 'filename' not in res or res['filename'] == '':
            self.flash(0, {'msg': '文件名称错误'})
            return

        ets = mimetypes.guess_all_extensions(res['content_type'])
        ext = os.path.splitext(res['filename'])[1].lower()
        if ets and ext not in ets:
            ext = ets[0]

        md5 = hashlib.md5()
        md5.update(res['body'])
        key = md5.hexdigest()

        dir = '/www'
        url = '/upload/' + self.timer().strftime('%Y/%m/%d/') + key[0] + key[1] + key[30] + key[31] + '/' + key + ext
        uri = self.settings['root_path'] + dir + url

        if not os.path.exists(os.path.dirname(uri)):
            os.makedirs(os.path.dirname(uri), mode=0777)

        fin = open(uri, 'w')
        fin.write(res['body'])
        fin.close()

        self.datum('files').affect(
                'insert into files (file_hash, file_base, file_path, file_type, file_memo, file_ctms) values (?, ?, ?, ?, ?, ?)',
                (key, dir, url, res['content_type'], res['filename'], self.stime()))

        if self.input('CKEditorFuncNum', None) is not None:
            out = '<script type="text/javascript">'
            out += 'window.parent.CKEDITOR.tools.callFunction(%s,"%s","%s");' % (self.input('CKEditorFuncNum'), url, '')
            out += '</script>'
            self.write(out)
        else:
            self.flash(1, {'msg': "上传成功", 'ext': {'url': url}})

class Admin_FileDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            fid = self.input('file_id')
            ctm = self.input('file_ctms')

            res = self.datum('files').single('select * from files where file_id = ?', (fid,))
            if not res:
                self.flash(0)
                return

            uri = self.settings['root_path'] + res['file_base'] + res['file_path']
            if os.path.isfile(uri):
                os.remove(uri)

                # Delete empty directories recursively
                dir = os.path.dirname(uri)
                while dir != self.settings['root_path'] and os.path.isdir(dir) and not os.listdir(dir):
                    os.rmdir(dir)
                    dir = os.path.dirname(dir)

            if self.datum('files').affect('delete from files where file_id = ? and file_ctms = ?', (fid, ctm)).rowcount:
                self.ualog(self.current_user, '删除文件：' + str(fid))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
