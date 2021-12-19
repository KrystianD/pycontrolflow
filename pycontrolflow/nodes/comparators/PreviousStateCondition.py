from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Any, TypeVar, Generic, Optional

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class PreviousStateCondition(Generic[TInput, TOutput], FlowSingleOutputNode[TOutput]):
    def __init__(self, input_name: FlowValue[TInput]) -> None:
        super().__init__()
        self.input_name = input_name

        self.prev_value: Optional[TInput] = None

    def reset_state(self) -> None:
        super().reset_state()
        self.prev_value = None

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_name.get()

        condition = self.process_values(self.prev_value, value)
        self.prev_value = value

        self.set_output(condition)

    @abstractmethod
    def process_values(self, prev_value: Optional[TInput], cur_value: Optional[TInput]) -> TOutput:
        pass
