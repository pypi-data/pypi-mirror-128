# pylint: skip-file
import unittest

import ioc

from .. import __ioc__


class InversionOfControlSetupTestCase(unittest.TestCase):

    def test_setup_ioc_returns_succesfully(self):
        __ioc__.setup_ioc()

    def test_setup_ioc_injects_josekeyresolver(self):
        __ioc__.setup_ioc()
        self.assertTrue(ioc.is_satisfied('JOSEKeyResolver'))
