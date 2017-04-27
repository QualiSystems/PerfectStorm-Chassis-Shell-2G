from mock import Mock
from unittest2 import TestCase

from bp_chassis.autoload.model.parent_aware import ParentAware


class TestParentAware(TestCase):
    def setUp(self):
        self._parent_id = Mock()
        self._instance = ParentAware(self._parent_id)

    def test_init(self):
        self.assertIs(self._instance._parent_id, self._parent_id)

    def test_parent_id_prop_getter(self):
        self.assertIs(self._instance.parent_id, self._parent_id)

    def test_parent_id_prop_setter(self):
        new_parent_id = Mock()
        self._instance.parent_id = new_parent_id
        self.assertIs(self._instance._parent_id, new_parent_id)
