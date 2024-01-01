from datetime import datetime, timedelta
from typing import TypeVar, Generic

from pycontrolflow.flow_value import FlowValue, wrap_input
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class Move(FlowNode, Generic[TValue]):
    def __init__(self, input_value: TNodeInput[TValue], output_value: FlowValue[TValue]) -> None:
        self._input_value = wrap_input(input_value)
        self._output_value = output_value

        super().__init__([self._input_value])

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        self._output_value.set(self._input_value.get())
