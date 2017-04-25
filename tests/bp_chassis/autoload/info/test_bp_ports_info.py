from mock import Mock, patch
from unittest2 import TestCase

from bp_chassis.autoload.info.bp_ports_info import BPPortsInfo


class TestBPPortsInfo(TestCase):
    def setUp(self):
        self._autoload_actions = Mock()
        self._logger = Mock()
        self._instance = BPPortsInfo(self._autoload_actions, self._logger)

    def test_init(self):
        self.assertIs(self._instance.autoload_actions, self._autoload_actions)
        self.assertIs(self._instance._logger, self._logger)

    @patch('bp_chassis.autoload.info.bp_ports_info.Module')
    @patch('bp_chassis.autoload.info.bp_ports_info.Port')
    def test_collect(self, port_class, module_class):
        pass
