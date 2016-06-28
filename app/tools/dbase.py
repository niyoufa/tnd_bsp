# -*- coding: UTF-8 -*-

import sys
reload(sys)

import os, glob

sys.setdefaultencoding('utf-8')
sys.path[0] = os.path.dirname(os.path.dirname(sys.path[0]))

from app.etc import etc
import sqlite3

def main():
    for sql in glob.glob(os.path.join(etc['database_path'], '*.sql')):
        sdb = sql[:-3] + 'sdb'
        if os.path.exists(sdb):
            print("Find dbase: %s" % sdb)
        else:
            print("Make dbase: %s" % sdb)

            con = sqlite3.connect(sdb)
            con.executescript(open(sql).read())
            con.close()

if __name__ == "__main__":
    main()

