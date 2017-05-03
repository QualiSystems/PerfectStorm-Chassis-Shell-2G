from mock import Mock
from unittest2 import TestCase

from bp_chassis.actions.autoload_actions import AutoloadActions


class TestAutoloadActions(TestCase):
    def setUp(self):
        self._rest_service = Mock()
        self._logger = Mock()
        self._instance = AutoloadActions(self._rest_service, self._logger)

    def test_get_ports_info(self):
        data = Mock()
        self._rest_service.request_get.return_value = data
        result = Mock()
        data.get.return_value = result
        self.assertIs(self._instance.get_ports_info(), result)
        uri = '/api/v1/bps/ports'
        self._rest_service.request_get.assert_called_once_with(uri)
        data.get.assert_called_once_with('portReservationState')
