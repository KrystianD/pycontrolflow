from datetime import datetime, timedelta
from typing import TypeVar, Generic

from pycontrolflow.flow_value import FlowValue, resolve_value
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class Move(FlowNode, Generic[TValue]):
    def __init__(self, input_name: TNodeInput[TValue], output_name: FlowValue[TValue]) -> None:
        super().__init__([])
        self.input_name = input_name
        self.output_name = output_name

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value(self.input_name)
        self.output_name.set(value)
