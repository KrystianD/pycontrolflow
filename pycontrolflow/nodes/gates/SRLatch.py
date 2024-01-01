from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class SRLatch(FlowSingleOutputNode[bool]):
    def __init__(self,
                 set_: TNodeInput[bool],
                 reset_: TNodeInput[bool],
                 nid: Optional[str] = None, persistent: bool = False) -> None:
        self._set = wrap_input(set_)
        self._reset = wrap_input(reset_)

        super().__init__([self._set, self._reset], nid=nid)

        self._persistent = persistent
        self._state_mem: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self._state_mem = self._create_memory("state", bool, False, self._persistent)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        set_ = self._set.get()
        reset_ = self._reset.get()

        if set_ is True and reset_ is False:
            self._state_mem.set(True)
        elif set_ is False and reset_ is True:
            self._state_mem.set(False)
        elif set_ is False and reset_ is False:
            pass
        else:
            raise Exception("invalid state, both S and R set")

        self.set_output(self._state_mem.get())
