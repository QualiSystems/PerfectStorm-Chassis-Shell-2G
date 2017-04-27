from mock import patch, Mock
from unittest2 import TestCase

from bp_chassis.autoload.model.bp_chassis_entities import Chassis, Module, Port


class TestChassis(TestCase):
    def setUp(self):
        self._resource_id = Mock()
        self._unique_identifier = Mock()
        self._parent_id = Mock()

    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_init(self, resource_init, parent_aware_init):
        _instance = Chassis(self._resource_id, self._unique_identifier, self._parent_id)
        resource_init.assert_called_once_with(_instance, self._resource_id, self._unique_identifier)
        parent_aware_init.assert_called_once_with(_instance, self._parent_id)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Chassis._get_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_version_prop_getter(self, resource_init, parent_aware_init, get_attribute):
        _instance = Chassis(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Version'
        attribute = Mock()
        get_attribute.return_value = attribute
        self.assertIs(attribute, _instance.version)
        get_attribute.assert_called_once_with(name)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Chassis._add_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_version_prop_setter(self, resource_init, parent_aware_init, add_attribute):
        _instance = Chassis(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Version'
        value = Mock()
        _instance.version = value
        add_attribute.assert_called_once_with(name, value)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Chassis._get_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_server_description_prop_getter(self, resource_init, parent_aware_init, get_attribute):
        _instance = Chassis(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Server Description'
        attribute = Mock()
        get_attribute.return_value = attribute
        self.assertIs(attribute, _instance.server_description)
        get_attribute.assert_called_once_with(name)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Chassis._add_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_server_description_prop_setter(self, resource_init, parent_aware_init, add_attribute):
        _instance = Chassis(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Server Description'
        value = Mock()
        _instance.server_description = value
        add_attribute.assert_called_once_with(name, value)


class TestModule(TestCase):
    def setUp(self):
        self._resource_id = Mock()
        self._unique_identifier = Mock()
        self._parent_id = Mock()

    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_init(self, resource_init, parent_aware_init):
        _instance = Module(self._resource_id, self._unique_identifier, self._parent_id)
        resource_init.assert_called_once_with(_instance, self._resource_id, self._unique_identifier)
        parent_aware_init.assert_called_once_with(_instance, self._parent_id)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Module._get_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_device_model_prop_getter(self, resource_init, parent_aware_init, get_attribute):
        _instance = Module(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Model'
        attribute = Mock()
        get_attribute.return_value = attribute
        self.assertIs(attribute, _instance.device_model)
        get_attribute.assert_called_once_with(name)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Module._add_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_device_model_prop_setter(self, resource_init, parent_aware_init, add_attribute):
        _instance = Module(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Model'
        value = Mock()
        _instance.device_model = value
        add_attribute.assert_called_once_with(name, value)


class TestPort(TestCase):
    def setUp(self):
        self._resource_id = Mock()
        self._unique_identifier = Mock()
        self._parent_id = Mock()

    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_init(self, resource_init, parent_aware_init):
        _instance = Port(self._resource_id, self._unique_identifier, self._parent_id)
        resource_init.assert_called_once_with(_instance, self._resource_id, self._unique_identifier)
        parent_aware_init.assert_called_once_with(_instance, self._parent_id)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Port._get_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_logical_name_prop_getter(self, resource_init, parent_aware_init, get_attribute):
        _instance = Port(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Logical Name'
        attribute = Mock()
        get_attribute.return_value = attribute
        self.assertIs(attribute, _instance.logical_name)
        get_attribute.assert_called_once_with(name)

    @patch('bp_chassis.autoload.model.bp_chassis_entities.Port._add_attribute')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.ParentAware.__init__')
    @patch('bp_chassis.autoload.model.bp_chassis_entities.Resource.__init__')
    def test_device_model_prop_setter(self, resource_init, parent_aware_init, add_attribute):
        _instance = Port(self._resource_id, self._unique_identifier, self._parent_id)
        name = 'Logical Name'
        value = Mock()
        _instance.logical_name = value
        add_attribute.assert_called_once_with(name, value)
