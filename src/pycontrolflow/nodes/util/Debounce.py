from datetime import timedelta, datetime
from typing import Optional, Any, Generic, TypeVar

from pycontrolflow.flow_value import FlowValue, FlowMemoryCell
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TValue = TypeVar("TValue")


class Debounce(FlowSingleOutputNode[TValue], Generic[TValue]):
    def __init__(self, input_name: FlowValue[Any], debounce_time: timedelta, nid: Optional[str] = None,
                 persistent: bool = False) -> None:
        super().__init__([input_name], nid=nid)
        self.input_name = input_name
        self.persistent = persistent

        self.debounce_time = debounce_time

        self._last_value: FlowMemoryCell[TValue] = None  # type: ignore
        self._last_change_date: FlowMemoryCell[datetime] = None  # type: ignore

    def setup(self) -> None:
        super().setup()
        self._last_value = self._create_memory("last_value", self.input_name.get_type(), self.input_name.get(),
                                               self.persistent)
        self._last_change_date = self._create_memory("last_change_date", datetime, datetime.min,
                                                     self.persistent)

    def reset_state(self) -> None:
        super().reset_state()
        self._last_change_date.set(datetime.min)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_name.get()

        diff = cur_date - self._last_change_date.get()
        if diff > self.debounce_time and value != self._last_value.get():
            self._last_value.set(value)
            self._last_change_date.set(cur_date)

        self.set_output(self._last_value.get())
