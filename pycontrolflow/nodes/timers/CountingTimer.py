from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import resolve_value, FlowMemoryCell
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class CountingTimer(FlowSingleOutputNode[bool]):
    def __init__(self, input_value: TNodeInput[bool], time: timedelta) -> None:
        super().__init__([input_value])
        self.input_value = input_value
        self.time = time

        self.condition_met_start: Optional[datetime] = None

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        value = resolve_value(self.input_value)
        output = False

        if value:
            if self.condition_met_start is None:
                self.condition_met_start = cur_date
            else:
                time_since_last_met = cur_date - self.condition_met_start

                if time_since_last_met > self.time:
                    output = True
        else:
            self.condition_met_start = None

        self.set_output(output)
