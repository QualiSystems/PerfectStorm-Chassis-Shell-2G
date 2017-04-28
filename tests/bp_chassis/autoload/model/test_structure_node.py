from collections import defaultdict

from mock import Mock, patch, PropertyMock
from unittest2 import TestCase, skip

from bp_chassis.autoload.model.structure_node import ValidatorInterface, IdValidator, RelativeAddress, StructureNode


class TestValidatorInterface(TestCase):
    def setUp(self):
        class TestedClass(ValidatorInterface):
            pass

        self._tested_class = TestedClass

    def test_init_abstract(self):
        with self.assertRaisesRegexp(TypeError, "Can't instantiate abstract class TestedClass"):
            self._tested_class()


class TestIdValidator(TestCase):
    def setUp(self):
        self._instance = IdValidator()

    def test_init(self):
        self.assertEqual(self._instance._paths, defaultdict(list))

    def test_registered(self):
        path_id = -1
        path_prefix = Mock()
        self.assertTrue(self._instance.registered(path_id, path_prefix))
        path_id = 1
        self.assertFalse(self._instance.registered(path_id, path_prefix))
        self._instance._paths[path_id].append(path_prefix)
        path_prefix1 = Mock()
        self.assertFalse(self._instance.registered(path_id, path_prefix1))
        self.assertTrue(path_prefix1 in self._instance._paths[path_id])
        self.assertTrue(self._instance.registered(path_id, path_prefix))

    def test_get_valid(self):
        self.assertEqual(self._instance.get_valid(), 0)
        self.assertEqual(self._instance.get_valid(), 1)
        self._instance._paths[3] = None
        self.assertEqual(self._instance.get_valid(), 4)


class TestRelativeAddress(TestCase):
    def setUp(self):
        self._path_id = Mock()
        self._path_prefix = Mock()
        self._instance = RelativeAddress(self._path_id, self._path_prefix)

    def test_init(self):
        self.assertIs(self._path_id, self._instance._path_id)
        self.assertIs(self._path_prefix, self._instance._path_prefix)
        self.assertIsNone(self._instance._parent_resource)
        self.assertIsNone(self._instance._valid_path_id)
        self.assertFalse(self._instance._duplicated)

    def test_parent_resource_prop_getter(self):
        parent_resource = Mock()
        self._instance._parent_resource = parent_resource
        self.assertIs(parent_resource, self._instance.parent_resource)

    def test_parent_resource_prop_setter_registered(self):
        parent_resource = Mock()
        parent_resource.id_validator.registered.return_value = True
        self._instance.parent_resource = parent_resource
        self.assertIs(parent_resource, self._instance._parent_resource)
        parent_resource.id_validator.registered.assert_called_once_with(self._path_id, self._path_prefix)
        self.assertTrue(self._instance._duplicated)

    def test_parent_resource_prop_setter_not_registered(self):
        parent_resource = Mock()
        parent_resource.id_validator.registered.return_value = False
        self._instance._parent_resource = parent_resource
        self.assertIs(parent_resource, self._instance._parent_resource)
        self.assertFalse(self._instance._duplicated)

    def test_valid_id_prop_getter_not_duplicated(self):
        self.assertIs(self._instance.valid_id, self._path_id)

    def test_valid_id_prop_getter_duplicated(self):
        self._instance._duplicated = True
        parent_resource = Mock()
        self._instance._parent_resource = parent_resource
        valid_id = Mock()
        parent_resource.id_validator.get_valid.return_value = valid_id
        self.assertIs(self._instance.valid_id, valid_id)
        parent_resource.id_validator.get_valid.assert_called_once_with()

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress.valid_id', new_callable=PropertyMock)
    def test_path_id_getter(self, valid_id):
        _instance = RelativeAddress(1, Mock())
        self.assertEqual(_instance.path_id, 1)
        mock_id = Mock()
        valid_id.return_value = mock_id
        _instance = RelativeAddress(-1, Mock())
        self.assertEqual(_instance.path_id, mock_id)

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress.valid_id', new_callable=PropertyMock)
    def test__local_path_prop_getter(self, valid_id):
        path_prefix = 'test'
        _instance = RelativeAddress(None, path_prefix)
        self.assertIsNone(_instance._local_path)
        mock_id = 1
        valid_id.return_value = mock_id
        _instance = RelativeAddress(mock_id, path_prefix)
        self.assertEqual(_instance._local_path, path_prefix + str(mock_id))
        _instance = RelativeAddress(mock_id, None)
        self.assertEqual(_instance._local_path, str(mock_id))

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress._local_path', new_callable=PropertyMock)
    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress.parent_resource', new_callable=PropertyMock)
    def test_build_path(self, parent_resource_prop, local_path_prop):
        relative_address = 'test_address'
        local_path = 'test_path'
        parent_resource = Mock()
        parent_resource.relative_address = relative_address
        parent_resource_prop.return_value = parent_resource
        local_path_prop.return_value = local_path
        self.assertEqual(self._instance._build_path(), '{0}/{1}'.format(relative_address, local_path))
        parent_resource_prop.return_value = None
        self.assertEqual(self._instance._build_path(), local_path)

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress._build_path')
    def test_value(self, build_path):
        path = Mock()
        build_path.return_value = path
        self.assertIs(self._instance.value, path)


class StructureNodeImplOverride(StructureNode):
    PREFIX = Mock()

    @property
    def _prefix(self):
        return self.PREFIX


class StructureNodeImplNoOverride(StructureNode):
    pass


class TestStructureNode(TestCase):
    def setUp(self):
        self._resource_id = Mock()

    def test_init_abstract(self):
        with self.assertRaisesRegexp(TypeError, "Can't instantiate abstract class StructureNodeImplNoOverride"):
            StructureNodeImplNoOverride(Mock())

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress')
    def test_init(self, relative_address_class):
        relative_address = Mock()
        relative_address_class.return_value = relative_address
        _instance = StructureNodeImplOverride(self._resource_id)
        relative_address_class.assert_called_once_with(path_id=self._resource_id,
                                                       path_prefix=StructureNodeImplOverride.PREFIX)
        self.assertIs(_instance._relative_address, relative_address)
        self.assertIsNone(_instance._id_validator)

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress')
    @patch('bp_chassis.autoload.model.structure_node.IdValidator')
    def test_id_validator(self, id_validator_class, relative_address_class):
        id_validator_instance = Mock()
        id_validator_class.return_value = id_validator_instance
        relative_address = Mock()
        relative_address_class.return_value = relative_address
        _instance = StructureNodeImplOverride(self._resource_id)
        self.assertIs(_instance.id_validator, id_validator_instance)
        id_validator_class.assert_called_once_with()
        self.assertIs(_instance.id_validator, id_validator_instance)
        id_validator_class.assert_called_once_with()

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress')
    def test_relative_address(self, relative_address_class):
        relative_address_inst = Mock()
        relative_address_value = Mock()
        relative_address_class.return_value = relative_address_inst
        relative_address_inst.value = relative_address_value
        _instance = StructureNodeImplOverride(self._resource_id)
        self.assertIs(_instance.relative_address, relative_address_value)

    @patch('bp_chassis.autoload.model.structure_node.RelativeAddress')
    def test_relative_address(self, relative_address_class):
        relative_address_inst = Mock()
        relative_address_class.return_value = relative_address_inst
        _instance = StructureNodeImplOverride(self._resource_id)
        parent = Mock()
        _instance.add_parent(parent)
        self.assertIs(relative_address_inst.parent_resource, parent)
