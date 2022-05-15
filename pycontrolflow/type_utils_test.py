import unittest

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.nodes.comparators.Changed import Changed
from pycontrolflow.nodes.comparators.Compare import CompareGreaterThan, Comparer
from pycontrolflow.nodes.comparators.EdgeFalling import EdgeFalling
from pycontrolflow.nodes.comparators.PreviousStateCondition import PreviousStateCondition
from pycontrolflow.type_utils import get_generic_args_for_obj


class TypeUtilsTest(unittest.TestCase):
    def test_typing_args(self) -> None:
        v = Changed[float](None)
        self.assertListEqual(get_generic_args_for_obj(v, PreviousStateCondition), [float, bool])
        self.assertListEqual(get_generic_args_for_obj(v, FlowSingleOutputNode), [bool])
        self.assertListEqual(get_generic_args_for_obj(v, IFlowValueProvider), [bool])

        v = CompareGreaterThan[float](0, 0)
        self.assertListEqual(get_generic_args_for_obj(v, Comparer), [float])
        self.assertListEqual(get_generic_args_for_obj(v, FlowSingleOutputNode), [bool])
        self.assertListEqual(get_generic_args_for_obj(v, IFlowValueProvider), [bool])

        v = EdgeFalling(False)
        self.assertListEqual(get_generic_args_for_obj(v, FlowSingleOutputNode), [bool])
        self.assertListEqual(get_generic_args_for_obj(v, IFlowValueProvider), [bool])


if __name__ == '__main__':
    unittest.main()
