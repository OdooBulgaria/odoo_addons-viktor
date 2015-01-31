# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import logging
import email

import os
import sys
import shutil
import glob
import os
import time
import datetime
import base64
import xmlrpclib


_logger = logging.getLogger(__name__)

from YaDiskClient import YaDisk
#disk = YaDisk(login, password)

#disk.df() # show used and available space
#disk.ls(path) # list of files/folder with attributes
#disk.mkdir(path) # create directory
#disk.rm(path) # delete file or directory
#disk.cp(src, dst) # copy from src to dst
#disk.mv(src, dst) # move from src to dst
#disk.upload(src, dst) # upload local file src to remote file dst
#disk.download(src, dst) # download remote file src to local file dst



_logger = logging.getLogger(__name__) # Need for message in console.
#_logger.warning("Task to email send = %s", send_task )

class fs_mover_all(osv.osv):


    _name = "fs.mover.all"
    _description = "File System Mover All"

    def files_from_to(self, cr, uid, ids, source_dir=None, dest_dir=None ,it_nulled=None,  context=None):

        res = {}
        if context is None: context = {}

        if source_dir is not None or dest_dir is not None:

            #source_dir = '/home/odoo/from'
            #dest_dir = '/home/odoo/to'

            now = time.strftime('%Y-%m-%d', time.localtime())

            for fname in glob.iglob(os.path.join(source_dir, "*.*")):
                modtime = os.stat(fname).st_mtime
                out = time.strftime('%Y-%m-%d', time.localtime(modtime))

                if out == now:

                    #shutil.copy2(fname, dest_dir)
                    shutil.move(fname,dest_dir)


        else:
            return False



        return True



    def backup_copy_today(self, cr, uid, ids, source_dir=None, dest_dir=None, it_nulled=None,  context=None):

        res = {}
        if context is None: context = {}

        if source_dir is not None or dest_dir is not None:

            #source_dir = '/home/odoo/from'
            #dest_dir = '/home/odoo/to'

            now = time.strftime('%Y-%m-%d', time.localtime())

            for fname in glob.iglob(os.path.join(source_dir, "*.*")):
                modtime = os.stat(fname).st_mtime
                out = time.strftime('%Y-%m-%d', time.localtime(modtime))

                if out == now:

                    shutil.copy2(fname, dest_dir)

        else:
            return False


        return True


    def backup_rpc_(self, cr, uid, ids, database = None, pw = None, context = None):


        sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/db')
        backup_file = open('backup.dump', 'wb')
        backup_file.write(base64.b64decode(sock.dump('mypassword', 'mydb')))
        backup_file.close()



    def backup_cm(self, cr, uid, backup_db, backup_pwd, backup_dir, context = None):

        sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/db')

        db_dump = base64.b64decode(sock.dump(backup_pwd, backup_db))

        filename = "%(db)s_%(timestamp)s.dump" % {
                'db': backup_db,
                'timestamp': datetime.datetime.utcnow().strftime(
                    "%Y-%m-%d_%H-%M-%SZ")
            }

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_file = open(os.path.join(backup_dir, filename), 'w')
        backup_file.write(db_dump)
        backup_file.close()



        disk = YaDisk('odoo.vladimir', 'OdooBack_345')

        _logger.warning("Yandex Disk space left: %s", disk.df() )

        #disk.mkdir('/test')

        disk.rm('/test')


        #result = self.disk.df()
        #self.assertIsInstance(result, dict)
        #self.assertTrue('available' in result.keys())
        #self.assertTrue('used' in result.keys())


#disk.df() # show used and available space
#disk.ls(path) # list of files/folder with attributes
#disk.mkdir(path) # create directory
#disk.rm(path) # delete file or directory
#disk.cp(src, dst) # copy from src to dst









#f = open("somefile.zip", "rb")
#g = open("thecopy.zip", "wb")

#while True:
#    buf = f.read(1024)
#    if len(buf) == 0:
#         break
#    g.write(buf)

#f.close()
#g.close()






#    def m2_backup(path, raise_exception=True):
#        path = os.path.normpath(path)
#        if not os.path.exists(path):
#            if not raise_exception:
#                return None
#        raise OSError('path does not exists')
#        cnt = 1
#        while True:
#            bck = '%s~%d' % (path, cnt)
#            if not os.path.exists(bck):
#                shutil.move(path, bck)
#                return bck
#        cnt += 1

#        try:
#            db_dump = base64.b64decode(
#                request.session.proxy("db").dump(backup_pwd, backup_db))
#            filename = "%(db)s_%(timestamp)s.dump" % {
#                'db': backup_db,
#                'timestamp': datetime.datetime.utcnow().strftime(
#                    "%Y-%m-%d_%H-%M-%SZ")
#            }
#            return request.make_response(db_dump,
#               [('Content-Type', 'application/octet-stream; charset=binary'),
#               ('Content-Disposition', content_disposition(filename))],
#               {'fileToken': token}
#            )
#        except Exception, e:
#            return simplejson.dumps([[],[{'error': openerp.tools.ustr(e), 'title': _('Backup Database')}]])











fs_mover_all()
