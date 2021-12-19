from datetime import datetime, timedelta
from typing import Any, TypeVar, Optional, Tuple, List

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TOutput = TypeVar("TOutput")


class Select(FlowSingleOutputNode[TOutput]):
    def __init__(self) -> None:
        super().__init__()

        self.conditions: List[Tuple[FlowValue[bool], Optional[TOutput]]] = []
        self.has_default = False
        self.default_value: Optional[TOutput] = None

    def case(self, cond1: FlowValue[bool], value1: Optional[TOutput]) -> 'Select[TOutput]':
        self.conditions.append((cond1, value1))
        return self

    def default(self, value: Optional[TOutput]) -> 'Select[TOutput]':
        self.has_default = True
        self.default_value = value
        return self

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        for cond, out_value in self.conditions:
            if cond.get() is True:
                self.set_output(out_value)
                return

        if self.has_default:
            self.set_output(self.default_value)
