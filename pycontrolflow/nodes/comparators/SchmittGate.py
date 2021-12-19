from datetime import datetime, timedelta
from typing import Optional

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowMemoryCell
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode


class SchmittGate(FlowSingleOutputNode[bool]):
    def __init__(self, input_name: IFlowValueProvider, low_value: float, high_value: float, initial: bool = False, invert: bool = False, nid: Optional[str] = None,
                 persistent: bool = False) -> None:
        super().__init__([input_name], nid=nid)
        self.input_name = input_name
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
        value = self.input_name.get()
        assert isinstance(value, float)

        if value > self.high_value:
            self.state.set(True)
        elif value < self.low_value:
            self.state.set(False)

        cur_state = self.state.get()
        assert cur_state is not None

        if self.invert:
            out_state = not cur_state
        else:
            out_state = cur_state

        self.set_output(out_state)
