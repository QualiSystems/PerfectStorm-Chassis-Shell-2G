from mock import Mock, patch, MagicMock, PropertyMock
from unittest2 import TestCase

from bp_chassis.autoload.model.autoload_elements import Attribute, Resource


class TestAttribute(TestCase):
    def setUp(self):
        self._attribute_name = Mock()
        self._attribute_value = Mock()
        self._relative_address = Mock()
        self._relative_address_value = Mock()
        self._relative_address.value = self._relative_address_value
        self._instance = Attribute(self._relative_address, self._attribute_name, self._attribute_value)

    def test_init(self):
        self.assertIs(self._instance._relative_address, self._relative_address)
        self.assertIs(self._instance.attribute_name, self._attribute_name)
        self.assertIs(self._instance.attribute_value, self._attribute_value)

    def test_relative_address_prop(self):
        self.assertIs(self._instance.relative_address, self._relative_address_value)

    @patch('bp_chassis.autoload.model.autoload_elements.AutoLoadAttribute')
    def test_autoload_attribute(self, autoload_attribute_class):
        attribute_instance = Mock()
        autoload_attribute_class.return_value = attribute_instance
        self.assertIs(attribute_instance, self._instance.autoload_attribute())
        autoload_attribute_class.assert_called_once_with(self._relative_address_value, self._attribute_name,
                                                         self._attribute_value)


class ResourceImpl(Resource):
    pass


class TestResource(TestCase):
    def setUp(self):
        self._resource_id = Mock()
        self._unique_identifier = 'unique_identifier'

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_init(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        structure_node_class.assert_called_once_with(_instance, self._resource_id)
        self.assertIs(_instance._unique_identifier, self._unique_identifier)
        self.assertEqual(_instance._attributes, {})

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_autoload_attributes(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        attribute = Mock()
        autoload_attribute = Mock()
        attribute.autoload_attribute.return_value = autoload_attribute
        _instance._attributes = {'test': attribute}
        self.assertEqual(_instance.autoload_attributes, [autoload_attribute])

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_prefix_prop(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        self.assertEqual(_instance._prefix, Resource.PREFIX)

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_model_prop(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        self.assertEqual(_instance.model, Resource.MODEL)

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_name_prop(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        relative_address = Mock()
        path_id = 'test_path_id'
        relative_address.path_id = path_id
        _instance._relative_address = relative_address
        self.assertEqual(_instance.name, Resource.NAME_TEMPLATE.format(path_id))

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_unique_identifier_prop(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        unique_identifier = Mock()
        _instance._unique_identifier = unique_identifier
        self.assertEqual(_instance.unique_identifier, unique_identifier)

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    @patch('bp_chassis.autoload.model.autoload_elements.Attribute')
    def test_add_attribute(self, attribute_class, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        relative_address = Mock()
        _instance._relative_address = relative_address
        name = 'test_name'
        value = 'test_value'
        attribute_instance = Mock()
        attribute_class.return_value = attribute_instance
        _instance._add_attribute(name, value)
        attribute_class.assert_called_once_with(relative_address, name, value)
        self.assertEqual({name: attribute_instance}, _instance._attributes)

    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_get_attribute(self, structure_node_class):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        name = 'test_name'
        value = 'test_value'
        attribute = Mock()
        attribute.attribute_value = value
        _instance._attributes = {name: attribute}
        self.assertIs(_instance._get_attribute(name), value)

    @patch('bp_chassis.autoload.model.autoload_elements.Resource.model', new_callable=PropertyMock)
    @patch('bp_chassis.autoload.model.autoload_elements.Resource.name', new_callable=PropertyMock)
    @patch('bp_chassis.autoload.model.autoload_elements.Resource.relative_address', new_callable=PropertyMock)
    @patch('bp_chassis.autoload.model.autoload_elements.Resource.unique_identifier', new_callable=PropertyMock)
    @patch('bp_chassis.autoload.model.autoload_elements.AutoLoadResource')
    @patch('bp_chassis.autoload.model.autoload_elements.StructureNode.__init__')
    def test_autoload_resource(self, structure_node_class, autoload_resource_class, unique_identifier_prop,
                               relative_address_prop, name_prop, model_prop):
        _instance = ResourceImpl(self._resource_id, self._unique_identifier)
        autoload_instance = Mock()
        autoload_resource_class.return_value = autoload_instance
        unique_identifier = Mock()
        unique_identifier_prop.return_value = unique_identifier
        relative_address = Mock()
        relative_address_prop.return_value = relative_address
        name = Mock()
        name_prop.return_value = name
        model = Mock()
        model_prop.return_value = model
        self.assertIs(autoload_instance, _instance.autoload_resource())
        autoload_resource_class.assert_called_once_with(model, name, relative_address, unique_identifier)
