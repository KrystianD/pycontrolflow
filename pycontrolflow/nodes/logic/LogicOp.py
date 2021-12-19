from datetime import datetime, timedelta
from typing import Iterable, Callable, List

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode


class LogicOp(FlowSingleOutputNode[bool]):
    def __init__(self, input_values: Iterable[IFlowValueProvider], op: Callable[[List[bool]], bool]) -> None:
        super().__init__(input_values)
        self.input_values = input_values
        self.op = op

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        input_values = [value.get() for value in self.input_values]

        for value in input_values:
            assert isinstance(value, bool)

        value = self.op(input_values)

        self.set_output(value)
