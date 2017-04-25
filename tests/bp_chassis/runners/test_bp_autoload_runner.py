from mock import Mock, patch, PropertyMock
from unittest2 import TestCase

from bp_chassis.runners.bp_autoload_runner import BPAutoloadRunner


class TestBpAutoloadRunner(TestCase):
    def setUp(self):
        self._context = Mock()
        self._logger = Mock()
        self._api = Mock()
        self._supported_os = Mock()
        self._instance = BPAutoloadRunner(self._context, self._logger, self._api, self._supported_os)

    @patch('bp_chassis.runners.bp_autoload_runner.BPAutoloadRunner._session_context_manager', new_callable=PropertyMock)
    @patch('bp_chassis.runners.bp_autoload_runner.BPAutoloadFlow')
    def test_autoload_flow_getter(self, autoload_flow_class, session_context_manager_prop):
        autoload_flow_instance = Mock()
        autoload_flow_class.return_value = autoload_flow_instance
        session = Mock()
        session_context_manager_prop.return_value = session
        self.assertIs(autoload_flow_instance, self._instance._autoload_flow)
        autoload_flow_class.assert_called_once_with(session, self._logger)

    @patch('bp_chassis.runners.bp_autoload_runner.BPAutoloadRunner._autoload_flow', new_callable=PropertyMock)
    def test_discover(self, autoload_flow_prop):
        autoload_flow = Mock()
        autoload_flow_prop.return_value = autoload_flow
        result = Mock()
        autoload_flow.autoload_details.return_value = result
        self.assertIs(result, self._instance.discover())
        autoload_flow.autoload_details.assert_called_once_with()
