from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import resolve_value_assert, resolve_value
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TValue = TypeVar("TValue")


class DLatch(FlowSingleOutputNode[TValue]):
    def __init__(self,
                 value: IFlowValueProvider[TValue],
                 enable: IFlowValueProvider[bool],
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([value, enable], nid=nid)
        self._value = value
        self._enable = enable

        self._persistent = persistent
        self._value_mem: FlowMemoryCell[TValue] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._value_mem = self._create_memory("state", self._value.get_type(), False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value(self._value)
        enable = resolve_value_assert(self._enable, bool, allow_null=False)

        if enable is True:
            self._value_mem.set(value)

        self.set_output(self._value_mem.get())
