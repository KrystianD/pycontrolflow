from datetime import datetime, timedelta
from typing import TypeVar, Union

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TValue = TypeVar("TValue")


class CompareGreaterThan(FlowSingleOutputNode[bool]):
    def __init__(self,
                 input1: Union[float, IFlowValueProvider],
                 input2: Union[float, IFlowValueProvider],
                 invert: bool = False) -> None:
        super().__init__([input1, input2])
        self.input1 = input1
        self.input2 = input2
        self.invert = invert

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = self.input1 if isinstance(self.input1, float) else self.input1.get()
        value2 = self.input2 if isinstance(self.input2, float) else self.input2.get()
        assert isinstance(value1, float)
        assert isinstance(value2, float)

        state = value1 > value2

        if self.invert:
            state = not state

        self.set_output(state)


class CompareLessThan(FlowSingleOutputNode[bool]):
    def __init__(self,
                 input1: Union[float, IFlowValueProvider],
                 input2: Union[float, IFlowValueProvider],
                 invert: bool = False) -> None:
        super().__init__([input1, input2])
        self.input1 = input1
        self.input2 = input2
        self.invert = invert

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value1 = self.input1 if isinstance(self.input1, float) else self.input1.get()
        value2 = self.input2 if isinstance(self.input2, float) else self.input2.get()
        assert isinstance(value1, float)
        assert isinstance(value2, float)

        state = value1 < value2

        if self.invert:
            state = not state

        self.set_output(state)
