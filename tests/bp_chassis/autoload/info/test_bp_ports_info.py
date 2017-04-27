from mock import Mock, patch
from unittest2 import TestCase, skip

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
        port_instance = Mock()
        module_instance = Mock()
        port_class.return_value = port_instance
        module_class.return_value = module_instance
        autoload_actions_result = "{[slot=2,port=0]=0, [slot=1,port=1]=1, [slot=2,port=1]=1, [slot=1,port=0]=0, [slot=2,port=2]=2}"
        self._autoload_actions.get_ports_info.return_value = autoload_actions_result
        expected_result = {'MOD1': module_instance,
                    'MOD2': module_instance,
                    'MOD1PORT1': port_instance,
                    'MOD1PORT0': port_instance,
                    'MOD2PORT0': port_instance,
                    'MOD2PORT1': port_instance,
                    'MOD2PORT2': port_instance}
        self.assertEqual(self._instance.collect(), expected_result)
