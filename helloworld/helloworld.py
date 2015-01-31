# -*- coding: utf-8 -*-

import logging

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


_logger = logging.getLogger(__name__)


class helloworld_test(osv.osv):

    def create(self, cr, uid, vals, context=None):
        context = dict(context or {})

        result = super(helloworld_test, self).create(cr, uid, vals, context)
        self.validate(cr, uid, [result], context=context)

        return result

    def write(self, cr, uid, ids, vals, context=None):

        if context is None:
            context = {}

        result = super(helloworld_test, self).write(cr, uid, ids, vals, context=context)
        self.validate(cr, uid, ids, context=context)

        return result

    _name = "helloworld.test"
    _description = "Helloworld Test"
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'value': fields.integer('Value', required=True),

    }

    def validate(self, cr, uid, ids, context=None):

        for check in self.browse(cr, uid, ids, context):

            if check.value <= 20:

                raise osv.except_osv(_('Error!'), _("Cannot save! You must select value over 20."))

    def create_helloworld(self, cr, uid, ids=False, context=None):

        context = dict(context or {})

        helloworld_test_obj = self.pool.get('helloworld.test')
        sequence_obj = self.pool.get('ir.sequence')

        name = sequence_obj.next_by_code(cr, uid, 'helloworld.test', context=context)

        helloworld_test_id = helloworld_test_obj.create(cr, uid, {
                    'name': name,
                    'value': 21
                }, context=context)

        _logger.debug("Hello World ID was created:(name- %s, ID - %s)", name, helloworld_test_id)

        return True

helloworld_test()

class helloworld_test2(osv.osv):

    _name = "helloworld.test2"
    _description = "Helloworld Test 2"
    _columns = {
        'name': fields.char('Name', required=True),
        'helloworld_test_id': fields.many2one('helloworld.test', 'Id', select=True),
    }

helloworld_test2()










