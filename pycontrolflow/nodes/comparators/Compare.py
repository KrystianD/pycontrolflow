from datetime import datetime, timedelta
from typing import TypeVar, Union

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowValue, resolve_value
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class CompareGreaterThan(FlowSingleOutputNode[bool]):
    def __init__(self,
                 input1: TNodeInput[float],
                 input2: TNodeInput[float],
                 invert: bool = False) -> None:
        super().__init__([input1, input2])
        self.input1 = input1
        self.input2 = input2
        self.invert = invert

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = resolve_value(self.input1)
        value2 = resolve_value(self.input2)
        assert isinstance(value1, float)
        assert isinstance(value2, float)

        state = value1 > value2

        if self.invert:
            state = not state

        self.set_output(state)


class CompareLessThan(FlowSingleOutputNode[bool]):
    def __init__(self,
                 input1: TNodeInput[float],
                 input2: TNodeInput[float],
                 invert: bool = False) -> None:
        super().__init__([input1, input2])
        self.input1 = input1
        self.input2 = input2
        self.invert = invert

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = resolve_value(self.input1)
        value2 = resolve_value(self.input2)
        assert isinstance(value1, float)
        assert isinstance(value2, float)

        state = value1 < value2

        if self.invert:
            state = not state

        self.set_output(state)
