from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class DLatch(FlowSingleOutputNode[TValue]):
    def __init__(self,
                 value: TNodeInput[TValue],
                 enable: TNodeInput[bool],
                 initial_state: Optional[TValue] = None,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        self._value = wrap_input(value)
        self._enable = wrap_input(enable)

        super().__init__([self._value, self._enable], nid=nid)

        self._initial_state = initial_state
        self._persistent = persistent
        self._value_mem: FlowMemoryCell[TValue] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._value_mem = self._create_memory("state", self._value.get_type(), self._initial_state, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self._value.get()
        enable = self._enable.get_notnull()

        if enable is True:
            self._value_mem.set(value)

        self.set_output(self._value_mem.get())
