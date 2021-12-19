from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import resolve_value_assert
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class DLatch(FlowSingleOutputNode[bool]):
    def __init__(self,
                 value: TNodeInput[bool],
                 enable: TNodeInput[bool],
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([value, enable], nid=nid)
        self._value = value
        self._enable = enable

        self._persistent = persistent
        self._state_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._state_mem = self._create_memory("state", bool, False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value_assert(self._value, bool, allow_null=False)
        enable = resolve_value_assert(self._enable, bool, allow_null=False)

        if enable is True:
            self._state_mem.set(value)

        self.set_output(self._state_mem.get())
