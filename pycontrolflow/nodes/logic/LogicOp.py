from datetime import datetime, timedelta
from typing import Callable, List, Sequence

from pycontrolflow.flow_value import resolve_value_assert_not_null, wrap_inputs
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class LogicOp(FlowSingleOutputNode[bool]):
    def __init__(self, input_values: Sequence[TNodeInput[bool]], op: Callable[[List[bool]], bool]) -> None:
        self.input_values = wrap_inputs(input_values)

        super().__init__(self.input_values)

        self.op = op

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        input_values = [value.get_notnull() for value in self.input_values]

        value = self.op(input_values)

        self.set_output(value)
