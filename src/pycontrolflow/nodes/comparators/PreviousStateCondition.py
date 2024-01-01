from abc import abstractmethod
from datetime import datetime, timedelta
from typing import TypeVar, Generic, Optional

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.mytypes import TNodeInput
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class PreviousStateCondition(FlowSingleOutputNode[TOutput], Generic[TInput, TOutput]):
    def __init__(self, input_: TNodeInput[TInput]) -> None:
        self.input_ = wrap_input(input_)

        super().__init__([self.input_])

        self.prev_value: Optional[TInput] = None

    def reset_state(self) -> None:
        super().reset_state()
        self.prev_value = None

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_.get()

        if self.prev_value is not None:
            condition = self.process_values(self.prev_value, value)
            self.set_output(condition)

        self.prev_value = value

    @abstractmethod
    def process_values(self, prev_value: TInput, cur_value: TInput) -> TOutput:
        pass
