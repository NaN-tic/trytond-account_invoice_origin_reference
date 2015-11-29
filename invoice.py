#This file is part account_invoice_origin_reference module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta


class InvoiceLine:
    __name__ = 'account.invoice.line'
    origin_reference_name = fields.Function(fields.Char('Origin Reference'),
        'get_origin_reference_name')

    @classmethod
    def get_origin_reference_name(cls, lines, name):
        '''
        From Invoice Line, get reference from parent line
        For example, if invoice line origin is sale line,
        return sale reference.
        '''
        res = {}
        for line in lines:
            reference = None
            if line.origin:
                origin = line.origin
                origin_str = str(line.origin)
                parent = origin_str.split('.')
                if parent and hasattr(origin, parent[0]):
                    p = getattr(origin, parent[0])
                    if hasattr(p, 'reference'):
                        reference = getattr(p, 'reference')
                    else:
                        reference = getattr(p, 'rec_name')
                else:
                    reference = origin.rec_name
            res[line.id] = reference
        return res
