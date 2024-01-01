from datetime import datetime, timedelta
from typing import TypeVar, Optional, Tuple, List, Generic

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TOutput = TypeVar("TOutput")


class Select(FlowSingleOutputNode[TOutput], Generic[TOutput]):
    def __init__(self) -> None:
        super().__init__([])

        self.conditions: List[Tuple[IFlowValueProvider[bool], IFlowValueProvider[TOutput]]] = []
        self.has_default = False
        self.default_value: Optional[IFlowValueProvider[TOutput]] = None

    def case(self, cond1: TNodeInput[bool], value1: TNodeInput[TOutput]) -> 'Select[TOutput]':
        cond1_ = wrap_input(cond1)
        value1_ = wrap_input(value1)

        self._register_provider(cond1_)
        self._register_provider(value1_)
        self.conditions.append((cond1_, value1_))
        return self

    def default(self, value: TNodeInput[TOutput]) -> 'Select[TOutput]':
        value_ = wrap_input(value)

        self._register_provider(value_)
        self.has_default = True
        self.default_value = value_
        return self

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        for cond, out_value in self.conditions:
            if cond.get() is True:
                self.set_output(out_value.get())
                return

        if self.has_default:
            assert self.default_value is not None
            self.set_output(self.default_value.get())
