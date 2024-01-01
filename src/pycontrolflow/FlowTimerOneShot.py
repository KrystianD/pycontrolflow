from datetime import timedelta
from typing import Optional

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.FlowTimer import FlowTimer
from pycontrolflow.flow_executor_helpers import var_for_node, memory_for_node
from pycontrolflow.read_only_flow_value import ReadOnlyFlowValue


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
        self._timer = memory_for_node(flow_executor, nid, "duration", timedelta, timedelta(), persistent=persistent)
        self._enabled = memory_for_node(flow_executor, nid, "enabled", bool, False, persistent=persistent)

        self.timer = ReadOnlyFlowValue(self._timer)
        self.enabled = ReadOnlyFlowValue(self._enabled)

    def _trigger(self) -> None:
        if self._enabled.get():
            if self._extend_on_trigger:
                self._timer.set(timedelta())  # reset timer
        else:
            self._timer.set(timedelta())  # reset timer
            self._enabled.set(True)

    def stop(self) -> None:
        self._timer.set(timedelta())  # reset timer
        self._enabled.set(False)

    def start_cycle(self) -> None:
        pass

    def process(self, delta: timedelta) -> None:
        if self._enabled.get():
            cur_duration = self._timer.get()
            assert cur_duration is not None
            self._timer.set(cur_duration + delta)

            if self._timer.get() >= self._duration:
                self._enabled.set(False)
                self._timer.set(self._duration)

    def process_after(self) -> None:
        if self.trigger.get() is True:
            self._trigger()
