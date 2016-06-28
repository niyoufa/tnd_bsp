# -*- coding: UTF-8 -*-

import os.path, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    base = os.path.dirname(os.path.dirname(sys.path[0]))
    dest = os.path.join(base, 'app', 'etc.py')
    etcs = os.path.join(base, 'doc', 'etc.py.sample')

    if not os.path.exists(dest):
        print("Make etc.py: %s => %s" % (etcs, dest))
        open(dest, 'wb').write(open(etcs, 'rb').read())
    else:
        print("Find etc.py: %s" % dest)

if __name__ == "__main__":
    main()

