from datetime import timedelta, datetime
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

        self.trigger = var_for_node(flow_executor, nid, "trigger", bool, False, run_on_update=self)
        self.reset = var_for_node(flow_executor, nid, "reset", bool, False, run_on_update=self)
        self._timer = memory_for_node(flow_executor, nid, "duration", timedelta, timedelta(), persistent=persistent)
        self._last_check_date = memory_for_node(flow_executor, nid, "last_check_date", datetime, datetime.min,
                                                persistent=persistent)
        self._enabled = memory_for_node(flow_executor, nid, "enabled", bool, False, persistent=persistent)

        self.timer = ReadOnlyFlowValue(self._timer)
        self.enabled = ReadOnlyFlowValue(self._enabled)

    def start_cycle(self) -> None:
        pass

    def update(self) -> None:
        if self.trigger.get():
            if self._extend_on_trigger:
                self._timer.set(timedelta())  # reset timer

            was_enabled = self._enabled.get()
            self._enabled.set(True)

            if self._extend_on_trigger or (not was_enabled and self._enabled.get()):
                self._last_check_date.set(datetime.min)

        if self.reset.get():
            self._timer.set(timedelta())  # reset timer
            self._enabled.set(False)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        self.update()

        if self._last_check_date.get() is datetime.min:
            self._last_check_date.set(cur_date)

        diff = cur_date - self._last_check_date.get()
        self._last_check_date.set(cur_date)

        if self._enabled.get():
            cur_duration = self._timer.get()
            self._timer.set(cur_duration + diff)

            if self._timer.get() >= self._duration:
                self._enabled.set(False)
                self._timer.set(self._duration)

    def process_after(self) -> None:
        pass
