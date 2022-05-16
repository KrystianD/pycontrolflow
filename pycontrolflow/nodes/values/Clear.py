from datetime import datetime, timedelta

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode


class Clear(FlowNode):
    def __init__(self, output_name: FlowValue[bool]) -> None:
        super().__init__([])
        self.output_name = output_name

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        self.output_name.set(False)
