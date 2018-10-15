#This file is part account_invoice_origin_reference module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from sql import Cast, Literal
from sql.functions import Substring, Position
from sql.operators import Like

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    origin_reference_name = fields.Function(fields.Char('Origin Reference'),
        'get_origin_reference_name', searcher='search_origin_reference_name')

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

    @classmethod
    def search_origin_reference_name(cls, name, clause):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        SaleLine = pool.get('sale.line')
        Sale = pool.get('sale.sale')
        PurchaseLine = pool.get('purchase.line')
        Purchase = pool.get('purchase.purchase')

        invoice_line = cls.__table__()
        invoice_line2 = cls.__table__()
        invoice = Invoice.__table__()
        sale_line = SaleLine.__table__()
        sale = Sale.__table__()
        purchase_line = PurchaseLine.__table__()
        purchase = Purchase.__table__()

        query = (invoice_line
            .join(invoice_line2, 'LEFT', condition=(
                    (Cast(Substring(invoice_line.origin,
                                Position(',', invoice_line.origin)
                        + Literal(1)), 'INTEGER') == invoice_line2.id)
                    &
                    (Like(invoice_line.origin, 'account.invoice.line,%'))
                    ))
            .join(invoice, 'LEFT', condition=(
                    invoice_line2.invoice == invoice.id
                    ))
            .join(sale_line, 'LEFT', condition=(
                    (Cast(Substring(invoice_line.origin,
                                Position(',', invoice_line.origin)
                        + Literal(1)), 'INTEGER') == sale_line.id)
                    &
                    (Like(invoice_line.origin, 'sale.line,%'))
                    ))
            .join(sale, 'LEFT', condition=(
                    sale_line.sale == sale.id
                    ))
            .join(purchase_line, 'LEFT', condition=(
                    (Cast(Substring(invoice_line.origin,
                                Position(',', invoice_line.origin)
                        + Literal(1)), 'INTEGER') == purchase_line.id)
                    &
                    (Like(invoice_line.origin, 'purchase.line,%'))
                    ))
            .join(purchase, 'LEFT', condition=(
                    purchase_line.purchase == purchase.id
                    ))
            .select(
                invoice_line.id,
                where=(
                    (Like(invoice.reference, clause[2]))
                    |
                    (Like(sale.reference, clause[2]))
                    |
                    (Like(purchase.reference, clause[2]))
                    )
                ))
        return [('id', 'in', query)]
