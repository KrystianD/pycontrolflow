from datetime import datetime, timedelta
from typing import Any, TypeVar, Optional, Tuple, List, Generic

from pycontrolflow.flow_value import FlowValue, resolve_value_notnull
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TOutput = TypeVar("TOutput")


class Select(FlowSingleOutputNode[TOutput], Generic[TOutput]):
    def __init__(self) -> None:
        super().__init__([])

        self.conditions: List[Tuple[TNodeInput[bool], TNodeInput[TOutput]]] = []
        self.has_default = False
        self.default_value: Optional[TNodeInput[TOutput]] = None

    def case(self, cond1: TNodeInput[bool], value1: TNodeInput[TOutput]) -> 'Select[TOutput]':
        self._register_provider(cond1)
        self._register_provider(value1)
        self.conditions.append((cond1, value1))
        return self

    def default(self, value: TNodeInput[TOutput]) -> 'Select[TOutput]':
        self._register_provider(value)
        self.has_default = True
        self.default_value = value
        return self

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        for cond, out_value in self.conditions:
            if resolve_value_notnull(cond) is True:
                self.set_output(resolve_value_notnull(out_value))
                return

        if self.has_default:
            assert self.default_value is not None
            self.set_output(resolve_value_notnull(self.default_value))
