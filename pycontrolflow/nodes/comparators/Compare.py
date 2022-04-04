from datetime import datetime, timedelta
from typing import TypeVar, Callable

from pycontrolflow.flow_value import resolve_value_notnull
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput, TComparable

TValue = TypeVar("TValue")


class Comparer(FlowSingleOutputNode[bool]):
    def __init__(self,
                 input1: TNodeInput[TValue],
                 input2: TNodeInput[TValue],
                 invert: bool,
                 op: Callable[[TValue, TValue], bool]) -> None:
        super().__init__([input1, input2])
        self._input1 = input1
        self._input2 = input2
        self._invert = invert
        self._op = op

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = resolve_value_notnull(self._input1)
        value2 = resolve_value_notnull(self._input2)
        assert type(value1) == type(value2)

        state = self._op(value1, value2)

        if self._invert:
            state = not state

        self.set_output(state)


class CompareGreaterThan(Comparer):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a > b)


class CompareGreaterEqualTo(Comparer):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: not a < b)


class CompareLessThan(Comparer):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a < b)


class CompareLessEqualTo(Comparer):
    def __init__(self, input1: TNodeInput[TComparable], input2: TNodeInput[TComparable], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: not a > b)
