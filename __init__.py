#This file is part account_invoice_origin_reference module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from trytond.pool import Pool
from .invoice import *


def register():
    Pool.register(
        InvoiceLine,
        module='account_invoice_origin_reference', type_='model')
