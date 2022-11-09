from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class MovingAverage(FlowSingleOutputNode[float]):
    def __init__(self, input_value: TNodeInput[float], ratio: float) -> None:
        self._input_value = wrap_input(input_value)

        super().__init__([self._input_value])
        self.ratio = ratio

        self._value = 0.0
        self._last_check_time: Optional[datetime] = None

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        value = self._input_value.get()

        if self._last_check_time is None:
            self._value = value
        else:
            diff = cur_date - self._last_check_time
            self._value += (value - self._value) * self.ratio * diff.total_seconds()

        self._last_check_time = cur_date

        self.set_output(self._value)
