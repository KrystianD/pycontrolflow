from datetime import datetime, timedelta, time
from typing import Union

from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.parse_utils import parse_time


class TimeCheck(FlowSingleOutputNode[bool]):
    def __init__(self, start_time: Union[time, str], end_time: Union[time, str]) -> None:
        super().__init__()
        self.start_time = parse_time(start_time)
        self.end_time = parse_time(end_time)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        if self.start_time < self.end_time:
            self.set_output(self.start_time <= cur_date.time() <= self.end_time)
        else:
            self.set_output(self.start_time <= cur_date.time() or cur_date.time() <= self.end_time)
