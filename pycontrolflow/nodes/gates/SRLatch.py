from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import resolve_value_assert
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class SRLatch(FlowSingleOutputNode[bool]):
    def __init__(self,
                 set: TNodeInput[bool],
                 reset: TNodeInput[bool],
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        super().__init__([set, reset], nid=nid)
        self._set = set
        self._reset = reset

        self._persistent = persistent
        self._state_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._state_mem = self._create_memory("state", bool, False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        set = resolve_value_assert(self._set, bool, allow_null=False)
        reset = resolve_value_assert(self._reset, bool, allow_null=False)

        if set is True and reset is False:
            self._state_mem.set(True)
        elif set is False and reset is True:
            self._state_mem.set(False)
        elif set is False and reset is False:
            pass
        else:
            raise Exception("invalid state, both S and R set")

        self.set_output(self._state_mem.get())
