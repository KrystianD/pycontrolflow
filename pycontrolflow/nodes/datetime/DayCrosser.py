from abc import abstractmethod
from datetime import datetime, timedelta, time
from typing import Union, Optional

from pycontrolflow.flow_value import FlowMemoryCell
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.parse_utils import parse_time


class DayCrosser(FlowSingleOutputNode[bool]):
    def __init__(self, cross_time: Optional[Union[time, str]] = None, persistent: bool = False, nid: Optional[str] = None) -> None:
        super().__init__([], nid=nid)
        self.cross_time = parse_time(cross_time) if cross_time is not None else time(0, 0, 0)
        self.persistent = persistent

        self.prev_date: FlowMemoryCell[datetime] = None  # type: ignore

    def setup(self) -> None:
        self.prev_date = self._create_memory("date", datetime, initial_value=datetime.min, persistent=self.persistent)

    def reset_state(self) -> None:
        super().reset_state()
        self.prev_date.set(None)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        if self.prev_date.get_notnull() == datetime.min:
            self.prev_date.set(cur_date)

        date_point = cur_date.replace(hour=self.cross_time.hour, minute=self.cross_time.minute, second=self.cross_time.second)

        self.set_output(self.prev_date.get_notnull() < date_point <= cur_date)

        self.prev_date.set(cur_date)

    def _get_output_type(self):
        return bool
