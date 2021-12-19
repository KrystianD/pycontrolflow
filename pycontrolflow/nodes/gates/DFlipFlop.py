from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import resolve_value_assert, resolve_value
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TValue = TypeVar("TValue")


class DFlipFlop(FlowSingleOutputNode[TValue]):
    def __init__(self,
                 value: IFlowValueProvider[TValue],
                 clock: IFlowValueProvider[bool],
                 initial_state: Optional[TValue] = None,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([value, clock], nid=nid)
        self._value = value
        self._clock = clock

        self._initial_state = initial_state
        self._persistent = persistent
        self._value_mem: FlowMemoryCell[TValue] = None  # type: ignore # filled in setup
        self._clock_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._value_mem = self._create_memory("value", self._value.get_type(), self._initial_state, self._persistent)
        self._clock_mem = self._create_memory("clock", bool, False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value(self._value)
        clock = resolve_value_assert(self._clock, bool, allow_null=False)

        prev_clock = self._clock_mem.get()
        if prev_clock is False and clock is True:
            self._value_mem.set(value)

        self._clock_mem.set(clock)

        self.set_output(self._value_mem.get())
