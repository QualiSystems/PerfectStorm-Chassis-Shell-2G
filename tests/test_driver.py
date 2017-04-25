from mock import patch, Mock
from unittest2 import TestCase

from driver import BreakingPointChassisDriver


class TestDriver(TestCase):
    def setUp(self):
        self._instance = BreakingPointChassisDriver()

    @patch('driver.get_logger_with_thread_id')
    @patch('driver.get_api')
    @patch('driver.BPAutoloadRunner')
    def test_get_inventory(self, bp_autoload_runner_class, get_api, get_logger_with_thread_id):
        context = Mock()
        logger = Mock()
        api = Mock()
        autoload_runner_instance = Mock()
        get_api.return_value = api
        get_logger_with_thread_id.return_value = logger
        bp_autoload_runner_class.return_value = autoload_runner_instance
        discover_result = Mock()
        autoload_runner_instance.discover.return_value = discover_result
        self.assertIs(discover_result, self._instance.get_inventory(context))
        get_logger_with_thread_id.assert_called_once_with(context)
        get_api.assert_called_once_with(context)
        bp_autoload_runner_class.assert_called_once_with(context, logger, api, self._instance.SUPPORTED_OS)
        autoload_runner_instance.discover.assert_called_once_with()
