from mock import Mock, patch
from unittest2 import TestCase

from bp_chassis.flows.bp_autoload_flow import BPAutoloadFlow


class ContextManagerMock(object):
    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestBPAutoloadFlow(TestCase):
    def setUp(self):
        self._session = Mock()
        self._session_context_manager = ContextManagerMock(self._session)
        self._logger = Mock()
        self._instance = BPAutoloadFlow(self._session_context_manager, self._logger)

    @patch('bp_chassis.flows.bp_autoload_flow.AutoloadActions')
    @patch('bp_chassis.flows.bp_autoload_flow.BPPortsInfo')
    @patch('bp_chassis.flows.bp_autoload_flow.BPAutoloadFlow._connect_elements')
    @patch('bp_chassis.flows.bp_autoload_flow.BPAutoloadFlow._build_autoload_details')
    def test_autoload_details(self, build_autoload_details_mth, connect_elements_mth, bp_ports_info_class,
                              autoload_actions_class):
        autoload_actions_instance = Mock()
        bp_ports_info_instance = Mock()
        autoload_details = Mock()
        autoload_actions_class.return_value = autoload_actions_instance
        bp_ports_info_class.return_value = bp_ports_info_instance
        build_autoload_details_mth.return_value = autoload_details
        elements = {Mock(): Mock()}
        bp_ports_info_instance.collect.return_value = elements
        self.assertIs(self._instance.autoload_details(), autoload_details)
        autoload_actions_class.assert_called_once_with(self._session, self._logger)
        bp_ports_info_class.assert_called_once_with(autoload_actions_instance, self._logger)
        bp_ports_info_instance.collect.assert_called_once_with()
        connect_elements_mth.assert_called_once_with(elements)
        build_autoload_details_mth.assert_called_once_with(elements)

    def test_connect_elements(self):
        key1 = Mock()
        value1 = Mock()
        key2 = Mock()
        value2 = Mock()
        value2.parent_id = key1
        elements = {key1: value1, key2: value2}
        self._instance._connect_elements(elements)
        value2.add_parent.assert_called_once_with(value1)
        value1.add_parent.assert_not_called()

    @patch('bp_chassis.flows.bp_autoload_flow.AutoLoadDetails')
    def test_build_autoload_details(self, autoload_details_class):
        key1 = Mock()
        value1 = Mock()
        key2 = Mock()
        value2 = Mock()
        value2.parent_id = key1
        attributes1 = [Mock()]
        attributes2 = [Mock()]
        value1.autoload_attributes = attributes1
        value2.autoload_attributes = attributes2
        value1.relative_address = None
        value2.relative_address = Mock()
        resource = Mock()
        value2.autoload_resource.return_value = resource
        elements = {key1: value1, key2: value2}
        autoload_instance = Mock()
        autoload_details_class.return_value = autoload_instance
        self.assertIs(autoload_instance, self._instance._build_autoload_details(elements))
        attributes = []
        attributes.extend(attributes1)
        attributes.extend(attributes2)
        autoload_details_class.assert_called_once_with([resource], attributes)
