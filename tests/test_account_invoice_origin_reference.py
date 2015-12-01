# This file is part of the account_invoice_origin_reference module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceOriginReferenceTestCase(ModuleTestCase):
    'Test Account Invoice Origin Reference module'
    module = 'account_invoice_origin_reference'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceOriginReferenceTestCase))
    return suite