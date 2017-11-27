#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `PerfectStormChassisDriver`
"""

import sys
import logging
import unittest

from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config, create_autoload_context

from driver import PerfectStormChassisDriver

address = '192.168.28.7'
user = 'admin'
admin_passowrd = 'DxTbqlSgAVPmrDLlHvJrsA=='


class TestPerfectStormChassisDriver(unittest.TestCase):

    def setUp(self):
        self.session = create_session_from_cloudshell_config()
        self.context = create_autoload_context(self.session, address=address, client_install_path='', controller='',
                                               port='', user=user, password=admin_passowrd)
        self.driver = PerfectStormChassisDriver()
        self.driver.initialize(self.context)
        print self.driver.logger.handlers[0].baseFilename
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def tearDown(self):
        pass

    def testHelloWorld(self):
        pass

    def testAutoload(self):
        self.inventory = self.driver.get_inventory(self.context)
        for r in self.inventory.resources:
            print r.relative_address, r.model, r.name
        for a in self.inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    sys.exit(unittest.main())
