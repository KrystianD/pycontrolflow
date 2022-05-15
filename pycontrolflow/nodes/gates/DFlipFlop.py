from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pycontrolflow.flow_value import resolve_value_assert, resolve_value, wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class DFlipFlop(FlowSingleOutputNode[TValue]):
    def __init__(self,
                 value: TNodeInput[TValue],
                 clock: TNodeInput[bool],
                 initial_state: Optional[TValue] = None,
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        self._value = wrap_input(value)
        self._clock = wrap_input(clock)

        super().__init__([self._value, self._clock], nid=nid)

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
        value = self._value.get()
        clock = self._clock.get_notnull()

        prev_clock = self._clock_mem.get()
        if prev_clock is False and clock is True:
            self._value_mem.set(value)

        self._clock_mem.set(clock)

        self.set_output(self._value_mem.get())
