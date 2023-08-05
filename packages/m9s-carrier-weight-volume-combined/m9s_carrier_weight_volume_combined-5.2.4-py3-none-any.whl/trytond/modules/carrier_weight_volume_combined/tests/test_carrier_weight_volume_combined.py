# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class CarrierWeightVolumeCombinedTestCase(ModuleTestCase):
    'Test Carrier Weight Volume Combined module'
    module = 'carrier_weight_volume_combined'
    extras = [
        'shipping',
        ]


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            CarrierWeightVolumeCombinedTestCase))
    return suite
