import typing
from abc import abstractmethod
from datetime import datetime, timedelta
from typing import TypeVar, Generic, Optional, Type

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class PreviousStateCondition(Generic[TInput, TOutput], FlowSingleOutputNode[TOutput]):
    def __init__(self, input_: TNodeInput[TInput]) -> None:
        self.input_ = wrap_input(input_)

        super().__init__([self.input_])

        self.prev_value: Optional[TInput] = None

    def reset_state(self) -> None:
        super().reset_state()
        self.prev_value = None

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.input_.get_notnull()

        if self.prev_value is not None:
            condition = self.process_values(self.prev_value, value)
            self.set_output(condition)

        self.prev_value = value

    @abstractmethod
    def process_values(self, prev_value: TInput, cur_value: TInput) -> TOutput:
        pass

    @classmethod
    def _get_input_type(cls) -> Type[TInput]:
        return typing.get_args(cls.__orig_bases__[0])[0]  # type: ignore

    @classmethod
    def _get_output_type(cls) -> Type[TOutput]:
        return typing.get_args(cls.__orig_bases__[0])[1]  # type: ignore
