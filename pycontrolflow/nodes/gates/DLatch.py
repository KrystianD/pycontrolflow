from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pycontrolflow.flow_value import resolve_value, resolve_value_assert_not_null
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class DLatch(FlowSingleOutputNode[TValue]):
    def __init__(self,
                 value: TNodeInput[TValue],
                 enable: TNodeInput[bool],
                 initial_state: Optional[TValue] = None,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([value, enable], nid=nid)
        self._value = value
        self._enable = enable

        self._initial_state = initial_state
        self._persistent = persistent
        self._value_mem: FlowMemoryCell[TValue] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._value_mem = self._create_memory("state", self._value.get_type(), self._initial_state, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value(self._value)
        enable = resolve_value_assert_not_null(self._enable, bool)

        if enable is True:
            self._value_mem.set(value)

        self.set_output(self._value_mem.get())
