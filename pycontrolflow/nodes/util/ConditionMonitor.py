from datetime import timedelta, datetime
from typing import Optional

from pycontrolflow.flow_value import FlowValue, FlowMemoryCell
from pycontrolflow.nodes.FlowNode import FlowNode


class ConditionMonitor(FlowNode):
    def __init__(self, input_name: FlowValue[bool], max_gap_time: timedelta, output_met: FlowValue[bool],
                 output_met_time: FlowValue[timedelta], nid: Optional[str] = None,
                 persistent: bool = False) -> None:
        super().__init__([input_name], nid=nid)
        self.input_name = input_name
        self.output_met = output_met
        self.output_met_time = output_met_time
        self.persistent = persistent

        self.max_gap_time = max_gap_time

        self.condition_met_start: FlowMemoryCell[datetime] = None  # type: ignore
        self.last_condition_met_date: FlowMemoryCell[datetime] = None  # type: ignore

    def setup(self) -> None:
        super().setup()
        self.condition_met_start = self.flow_executor.memory("met_start", datetime, datetime.min, self.persistent)
        self.last_condition_met_date = self.flow_executor.memory("last_met_date", datetime, datetime.min,
                                                                 self.persistent)

    def reset_state(self) -> None:
        super().reset_state()
        self.last_condition_met_date.set(datetime.min)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_name.get()
        assert isinstance(value, bool)

        if self.last_condition_met_date.get_notnull() != datetime.min:
            time_since_last_met = cur_date - self.last_condition_met_date.get_notnull()

            if time_since_last_met > self.max_gap_time:
                self.condition_met_start.set(datetime.min)

        if value:
            if self.condition_met_start.get_notnull() == datetime.min:
                self.condition_met_start.set(cur_date)

            self.last_condition_met_date.set(cur_date)

        if self.output_met is not None:
            self.output_met.set(self.condition_met_start.get_notnull() != datetime.min)

        if self.output_met_time is not None:
            if self.condition_met_start.get_notnull() == datetime.min:
                self.output_met_time.set(timedelta())
            else:
                self.output_met_time.set(cur_date - self.condition_met_start.get_notnull())
