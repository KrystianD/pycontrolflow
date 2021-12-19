from datetime import timedelta
from typing import Optional

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.FlowTimer import FlowTimer


class FlowTimerOneShot(FlowTimer):
    def __init__(self, flow_executor: FlowExecutor,
                 name: str, duration: timedelta, extend_on_trigger: bool,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__(name)
        self.duration = duration
        self.extend_on_trigger = extend_on_trigger
        self.nid = nid
        self.persistent = persistent

        self.timer = flow_executor._memory_for_node(nid, "duration", timedelta, timedelta(), persistent=persistent)
        self.enabled = flow_executor._memory_for_node(nid, "enabled", bool, False, persistent=persistent)

    def trigger(self) -> None:
        if self.enabled.get():
            if self.extend_on_trigger:
                self.timer.set(timedelta())  # reset timer
        else:
            self.timer.set(timedelta())  # reset timer
            self.enabled.set(True)

    def stop(self) -> None:
        self.timer.set(timedelta())  # reset timer
        self.enabled.set(False)

    def start_cycle(self) -> None:
        pass

    def process(self, delta: timedelta) -> None:
        if self.enabled.get():
            cur_duration = self.timer.get()
            assert cur_duration is not None
            self.timer.set(cur_duration + delta)

            if self.timer.get_notnull() >= self.duration:
                self.enabled.set(False)
                self.timer.set(self.duration)
