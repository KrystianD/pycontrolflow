from datetime import timedelta
from typing import Optional

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.FlowTimer import FlowTimer
from pycontrolflow.flow_executor_helpers import var_for_node, memory_for_node


class FlowTimerOneShot(FlowTimer):
    def __init__(self, flow_executor: FlowExecutor,
                 name: str, duration: timedelta, extend_on_trigger: bool,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__(name)
        self._duration = duration
        self._extend_on_trigger = extend_on_trigger
        self._nid = nid
        self._persistent = persistent

        self.trigger = var_for_node(flow_executor, nid, "trigger", bool, False)
        self.timer = memory_for_node(flow_executor, nid, "duration", timedelta, timedelta(), persistent=persistent)
        self.enabled = memory_for_node(flow_executor, nid, "enabled", bool, False, persistent=persistent)

    def _trigger(self) -> None:
        if self.enabled.get():
            if self._extend_on_trigger:
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

            if self.timer.get() >= self._duration:
                self.enabled.set(False)
                self.timer.set(self._duration)

    def process_after(self) -> None:
        if self.trigger.get() is True:
            self._trigger()
