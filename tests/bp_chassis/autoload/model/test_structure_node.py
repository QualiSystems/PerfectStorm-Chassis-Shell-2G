from collections import defaultdict

from mock import Mock
from unittest2 import TestCase

from bp_chassis.autoload.model.structure_node import ValidatorInterface, IdValidator


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
