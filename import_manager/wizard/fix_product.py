# -*- coding: utf-8 -*-

import logging

from openerp import models, fields, api
from openerp.tools.translate import _

from datetime import datetime

_logger = logging.getLogger(__name__) # Need for message in console.


class FixProduct(models.TransientModel):

    _name = 'fix.product'
    _description = 'Fix Internal category from POS category'


    @api.one
    def check_product_cat(self):

        #_logger.warning("Cat ID = %s, Cat Name = %s", self.first_pos_cat_id.id, self.first_pos_cat_id.name)

        product_product_obj = self.env['product.product']

        product_category_obj = self.env['product.category']
        pos_category_obj = self.env['pos.category']

        product_product_search = product_product_obj.search([('active', '=', True)])

        for product in product_product_search:

            product_cat_name = product.categ_id.name
            pos_cat_name = product.pos_categ_id.name

            if product_cat_name != pos_cat_name and pos_cat_name != False:

                product_category_search = product_category_obj.search([('name', '=', pos_cat_name)])

                _logger.warning("Product: name = %s, code = %s", product.name, product.default_code )
                _logger.warning("Product Category: ID = %s, name = %s, pos_cat. = %s", product_category_search.id, product_category_search.name, pos_cat_name )

                product.write({'categ_id': product_category_search.id })

        #product_product_search = product_product_obj.search([('pos_categ_id', '=', self.first_pos_cat_id.id)])
        #product_product_search.write({'pos_categ_id': self.second_pos_cat_id.id })

        return True

