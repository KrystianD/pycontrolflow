from datetime import datetime, timedelta
from typing import TypeVar

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode

TInput = TypeVar("TInput")


class MoveValue(FlowNode):
    def __init__(self, value: TInput, output_name: FlowValue[TInput]) -> None:
        super().__init__()
        self.value = value
        self.output_name = output_name

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        self.output_name.set(self.value)
