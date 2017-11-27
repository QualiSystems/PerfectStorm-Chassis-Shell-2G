#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `STCShellDriver`
"""

import sys
import unittest

from cloudshell.api.cloudshell_api import ResourceAttributesUpdateRequest, AttributeNameValue
from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config

stc_chassis = {'perfectstorm': {'address': '192.168.28.7',
                                'controller': '',
                                'port': '',
                                'install_path': '',
                                'user': 'admin',
                                'password': 'admin',
                                'modules': 1,
                                }
               }


class TestIxiaChassisShell(unittest.TestCase):

    session = None

    def setUp(self):
        self.session = create_session_from_cloudshell_config()

    def tearDown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def testHelloWorld(self):
        pass

    def test_perfectstorm(self):
        self._get_inventory('perfectstorm', stc_chassis['perfectstorm'])

    def _get_inventory(self, name, properties):
        self.resource = self.session.CreateResource(resourceFamily='Traffic Generator Chassis',
                                                    resourceModel='PerfectStorm Chassis',
                                                    resourceName=name,
                                                    resourceAddress=properties['address'],
                                                    folderFullPath='Testing',
                                                    parentResourceFullPath='',
                                                    resourceDescription='should be removed after test')
        self.session.UpdateResourceDriver(self.resource.Name, 'PerfectStormChassisDriver')
        attributes = [AttributeNameValue('Controller Address', properties['controller']),
                      AttributeNameValue('User', properties['user']),
                      AttributeNameValue('Password', properties['password'])]
        self.session.SetAttributesValues(ResourceAttributesUpdateRequest(self.resource.Name, attributes))
        self.session.AutoLoad(self.resource.Name)
        resource_details = self.session.GetResourceDetails(self.resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(self.resource.Name)


if __name__ == '__main__':
    sys.exit(unittest.main())
