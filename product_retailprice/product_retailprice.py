# -*- coding: utf-8 -*-
#from osv import fields, osv

import math
import re
import logging
import openerp.addons.decimal_precision as dp
#import openerp.addons.product.pricelist

#from _common import rounding
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


_logger = logging.getLogger(__name__) # Need for message in console.



class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {
         # For display retailprice in product.

       'retail_price': fields.float('Retail Price', digits_compute=dp.get_precision('Product Price'), help="Retail price."),

        }

product_template()












