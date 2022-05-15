from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.flow_value import FlowMemoryCell, wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput


class SchmittGate(FlowSingleOutputNode[bool]):
    def __init__(self, input_: TNodeInput[float], low_value: float, high_value: float, initial: bool = False, invert: bool = False, nid: Optional[str] = None,
                 persistent: bool = False) -> None:
        input_wrap = wrap_input(input_)
        super().__init__([input_wrap], nid=nid)
        self.input_ = input_wrap
        self.low_value = low_value
        self.high_value = high_value
        self.initial = initial
        self.invert = invert
        self.persistent = persistent

        self.state_default = initial if not invert else not initial
        self.state: FlowMemoryCell[bool] = None  # type: ignore # filled in setup

    def setup(self) -> None:
        super().setup()
        self.state = self._create_memory("state", bool, self.state_default, self.persistent)

    def reset_state(self) -> None:
        super().reset_state()
        self.state.set(self.state_default)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_.get_notnull()

        if value > self.high_value:
            self.state.set(True)
        elif value < self.low_value:
            self.state.set(False)

        cur_state = self.state.get_notnull()
        assert cur_state is not None

        if self.invert:
            out_state = not cur_state
        else:
            out_state = cur_state

        self.set_output(out_state)
