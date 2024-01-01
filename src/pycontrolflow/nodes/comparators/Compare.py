from datetime import datetime, timedelta
from typing import TypeVar, Callable, Generic

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.type_utils import is_same_type
from pycontrolflow.types import TNodeInput, TComparable

TValue = TypeVar("TValue")


class Comparer(FlowSingleOutputNode[bool], Generic[TValue]):
    def __init__(self,
                 input1: TNodeInput[TValue],
                 input2: TNodeInput[TValue],
                 invert: bool,
                 op: Callable[[TValue, TValue], bool]) -> None:
        input1_wrap = wrap_input(input1)
        input2_wrap = wrap_input(input2)

        super().__init__([input1_wrap, input2_wrap])

        input1_type = input1_wrap.get_type()
        input2_type = input2_wrap.get_type()

        if not is_same_type(input1_type, input2_type):
            raise TypeError(f"Comparer types mismatch, got: {input1_type} and {input2_type}")

        self._input1 = input1_wrap
        self._input2 = input2_wrap
        self._invert = invert
        self._op = op

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = self._input1.get()
        value2 = self._input2.get()

        state = self._op(value1, value2)

        if self._invert:
            state = not state

        self.set_output(state)


class CompareGreaterThan(Comparer[TComparable], Generic[TComparable]):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a > b)


class CompareGreaterEqualTo(Comparer[TComparable], Generic[TComparable]):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: not a < b)


class CompareLessThan(Comparer[TComparable], Generic[TComparable]):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a < b)


class CompareLessEqualTo(Comparer[TComparable], Generic[TComparable]):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: not a > b)
