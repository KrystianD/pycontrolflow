from datetime import datetime, timedelta
from typing import TypeVar, Union, Callable

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowValue, resolve_value
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

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
        value1 = resolve_value(self._input1)
        value2 = resolve_value(self._input2)
        assert type(value1) == type(value2)

        state = self._op(value1, value2)

        if self._invert:
            state = not state

        self.set_output(state)


class CompareGreaterThan(Comparer[bool]):
    def __init__(self, input1: TNodeInput[TValue], input2: TNodeInput[TValue], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a > b)


class CompareGreaterEqualTo(Comparer[bool]):
    def __init__(self, input1: TNodeInput[TValue], input2: TNodeInput[TValue], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a >= b)


class CompareLessThan(Comparer[bool]):
    def __init__(self, input1: TNodeInput[TValue], input2: TNodeInput[TValue], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a < b)


class CompareLessEqualTo(Comparer[bool]):
    def __init__(self, input1: TNodeInput[TValue], input2: TNodeInput[TValue], invert: bool = False) -> None:
        super().__init__(input1, input2, invert, lambda a, b: a <= b)
