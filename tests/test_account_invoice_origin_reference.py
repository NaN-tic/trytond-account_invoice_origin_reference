#!/usr/bin/env python
#This file is part account_invoice_origin_reference module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends


class AccountInvoiceOriginReferenceTestCase(unittest.TestCase):
    'Test Account Invoice Origin Reference module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_invoice_origin_reference')

    def test0005views(self):
        'Test views'
        test_view('account_invoice_origin_reference')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceOriginReferenceTestCase))
    return suite
