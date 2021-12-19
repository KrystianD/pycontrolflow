from datetime import datetime, timedelta
from typing import TypeVar

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode

TInput = TypeVar("TInput")


class Move(FlowNode):
    def __init__(self, input_name: FlowValue[TInput], output_name: FlowValue[TInput]) -> None:
        super().__init__()
        self.input_name = input_name
        self.output_name = output_name

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_name.get()
        self.output_name.set(value)
