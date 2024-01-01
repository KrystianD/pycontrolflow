from datetime import datetime, timedelta

from pycontrolflow.FlowTimerOneShot import FlowTimerOneShot
from pycontrolflow.nodes.FlowNode import FlowNode


class TimerTrigger(FlowNode):
    def __init__(self, timer: FlowTimerOneShot) -> None:
        super().__init__([])
        self.timer = timer

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        self.timer._trigger()
