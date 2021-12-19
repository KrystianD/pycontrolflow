from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import resolve_value_assert
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class DFlipFlop(FlowSingleOutputNode[bool]):
    def __init__(self,
                 value: TNodeInput[bool],
                 clock: TNodeInput[bool],
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([value, clock], nid=nid)
        self._value = value
        self._clock = clock

        self._persistent = persistent
        self._state_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup
        self._clock_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._state_mem = self._create_memory("state", bool, False, self._persistent)
        self._clock_mem = self._create_memory("clock", bool, False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = resolve_value_assert(self._value, bool, allow_null=False)
        clock = resolve_value_assert(self._clock, bool, allow_null=False)

        prev_clock = self._clock_mem.get()
        if prev_clock is False and clock is True:
            self._state_mem.set(value)

        self._clock_mem.set(clock)

        self.set_output(self._state_mem.get())
