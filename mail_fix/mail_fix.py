# -*- coding: utf-8 -*-
#from osv import fields, osv

#import math
#import re
#import logging
#import openerp.addons.decimal_precision as dp
#import openerp.addons.product.pricelist

#from _common import rounding
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import models, api

#_logger = logging.getLogger(__name__) # Need for message in console.




class FooterlessNotification(models.Model):
    _inherit = 'mail.notification'

    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        return ""












