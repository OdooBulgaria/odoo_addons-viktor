# -*- coding: utf-8 -*-


import logging

import os
import sys
import shutil
import glob
import os



import base64
import xmlrpclib


import time
import datetime
from dateutil import tz

import pytz

import openerp.exceptions


from dateutil import parser


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
from openerp import netsvc
import openerp.tools as tools

from openerp import models, api

import os
import csv

import re
import io
import codecs

import itertools
import operator

import math
import re
import time
from collections import OrderedDict

_logger = logging.getLogger(__name__) # Need for message in console.

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def add_check_digit(upc_str):
    """
    Returns a 12 digit upc-a string from an 11-digit upc-a string by adding
    a check digit

    >>> add_check_digit('02345600007')
    '023456000073'
    >>> add_check_digit('21234567899')
    '212345678992'
    >>> add_check_digit('04210000526')
    '042100005264'
    """

    upc_str = str(upc_str)
    if len(upc_str) != 11:
        return -1

    odd_sum = 0
    even_sum = 0
    for i, char in enumerate(upc_str):
        j = i+1
        if j % 2 == 0:
            even_sum += int(char)
        else:
            odd_sum += int(char)

    total_sum = (odd_sum * 3) + even_sum
    mod = total_sum % 10
    check_digit = 10 - mod
    if check_digit == 10:
        check_digit = 0
    return upc_str + str(check_digit)


class CheckEANProduct(osv.osv):

    _name = 'check.ean.product'
    _columns = {
                    'name': fields.char('Name', size=100, required='True'),
                    'path': fields.char('Path for import', size=100, required='True'),
                }


    def _log_file(self, cr, uid, l_file, rwa, l_messagem): # File name , Type accees to file r- read, w - write, a - append, Text message

        try:
            log_file = codecs.open(l_file, rwa, encoding='utf-8')
        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source log', message="Error: %s " %(ierror))

        #_logger.warning("Error: %s", l_messagem )
        log_file.write(l_messagem + os.linesep)
        log_file.close()


    def _check_double(self, cr, uid, source_dir, filename): #Detect Double ID in first row.

        keys = []

        try:
            import_file = codecs.open(os.path.join(source_dir, filename), 'r', encoding='utf-8')

        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source double', message="Error: %s " %( ierror ))

        csvData = csv.reader(utf_8_encoder(import_file))
        #csvData = csv.DictReader(utf_8_encoder(import_file))

#Add header for log file
        filename_log_double = filename+'__import_log_double.csv'
        source_log_double = os.path.join(source_dir, filename_log_double)
        self._log_file(cr, uid, source_log_double, 'w', '"0","1","2","3"' )

#Check double key in csv: exmp: 0 column ean key

        for key, grp in itertools.groupby(sorted(csvData, key=operator.itemgetter(0)), key=operator.itemgetter(0)):
            rowss = list(grp)

            if len(rowss) > 1:
                #_logger.warning("Double: %s", key )
                keys.append(key)

                for row in rowss:

                    string = '%s,"%s","%s","%s"' % (row[0], row[1], row[2], row[3])

                    self._log_file(cr, uid, source_log_double, 'a', string )

        import_file.close()

        if keys > 0: #if not search double return Fasle, esle True
            return True
        else:
            return False


    def _fix_csv(self, cr, uid, source_dir, filename): #Clean double or white space in column ID (0).

        p_keys = []

        try:
            open_file = codecs.open(os.path.join(source_dir, filename), 'r', encoding='utf-8')
            open_file_double = codecs.open(os.path.join(source_dir, filename+'__import_log_double.csv'), 'r', encoding='utf-8')

        except Exception, e:
             ierror = tools.ustr(e)
             return self.pool.get('warning').info(cr, uid, title='Error source for FIX', message="Error: %s " %( ierror ))

        csv_data = csv.reader(utf_8_encoder(open_file))
        csv_data_double = csv.reader(utf_8_encoder(open_file_double))

        row_num_d = 0
        for row in csv_data_double:
            if row_num_d > 0:
                p_keys.append(row[0])

            row_num_d += 1

        p_keys.append(" ")
        p_keys.append("")

        #_logger.warning("Double keys: %s", p_keys )


#add header to new file
        filename_fix = filename+'__fix.csv'
        source_fix = os.path.join(source_dir, filename_fix)
        self._log_file(cr, uid, source_fix, 'w', '"Internal Reference","DESCRIPTION","PRICE","POS Category","Detect","New UPC"' )

        row_num = 0

        for row in csv_data:
            if row_num > 0:
                imp_ref = row[0]
                imp_name = row[1].decode('utf-8')
                imp_price = row[2]
                imp_pos_cat = row[3]
                imp_det = ""
                new_upc = ""

                zero_imp_ref = ""

                if imp_ref in p_keys:
                    imp_det = "D"

                if len(imp_ref) == 10: # if 10 chars in code

                    zero_imp_ref = '0%s' % (imp_ref)
                    new_upc = add_check_digit(zero_imp_ref) # generate new UPC id

                elif len(imp_ref) == 11: #if 11 chars in code

                    new_upc = add_check_digit(imp_ref)

                elif len(imp_ref) < 10: # if < 10 chars in code

                    zero_d = 11 - len(imp_ref)


                    zero_imp_ref = imp_ref

                    for i in range(0,zero_d):
                        zero_imp_ref = '0%s' % (zero_imp_ref) # added Zeroo before id to 11 chars

                    new_upc = add_check_digit(zero_imp_ref)

                else:
                    imp_det = imp_det+"%s" % "E"

                #_logger.warning(" Original ID = %s, OLD ID = %s, New ID: %s", imp_ref, zero_imp_ref, new_upc  )
                string = '%s,"%s","%s","%s","%s","%s"' % (imp_ref, imp_name, imp_price,imp_pos_cat, imp_det, new_upc)

                self._log_file(cr, uid, source_fix, 'a', string )

            row_num += 1

        return True


    def ean_check(self, cr, uid, ids, context=None):

        context = dict(context or {})
#Get import paramets
        check_ean_obj = self.pool.get('check.ean.product')
        check_ean_data = check_ean_obj.browse(cr, uid, ids, context=context)

        file_name = check_ean_data.name
        dir_path = check_ean_data.path

        filename = file_name
        source_dir = dir_path

        self._check_double(cr, uid, source_dir, filename) # check double ID

        self._fix_csv(cr, uid, source_dir, filename) # Mark double and empty ID. Fix UPC ID.

















