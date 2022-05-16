from datetime import timedelta, datetime
from typing import Iterable, List, Optional, TYPE_CHECKING, Type, Any, TypeVar, Sequence

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowMemoryCell
from pycontrolflow.string_utils import random_string
from pycontrolflow.types import TNodeInput

if TYPE_CHECKING:
    from pycontrolflow.Flow import Flow
    from pycontrolflow.FlowExecutor import FlowExecutor
    from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

T = TypeVar("T")


class FlowNode:
    def __init__(self, providers: Sequence[IFlowValueProvider[Any]], nid: Optional[str] = None) -> None:
        self.nid = nid
        self.providers: Sequence[IFlowValueProvider[Any]] = providers
        self.flow_executor: 'FlowExecutor' = None  # type: ignore

        self.subflows: List['Flow'] = []

    def set_executor(self, flow_executor: 'FlowExecutor') -> None:
        self.flow_executor = flow_executor
        for provider in self.providers:
            if isinstance(provider, FlowNode):
                provider.set_executor(flow_executor)

    def register_subflow(self, flow: Optional['Flow']) -> None:
        if flow is not None:
            self.subflows.append(flow)

    # called after flow executor injected dependencies
    def setup(self) -> None:
        from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

        for provider in self.providers:
            self._register_provider(provider)

    def reset_state(self) -> None:
        for provider in self.providers:
            if isinstance(provider, FlowNode):
                provider.reset_state()

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        for provider in self.providers:
            if isinstance(provider, FlowNode):
                provider.process(cur_date, delta)

    def _create_memory(self, name: str, var_type: Type[T], initial_value: T, persistent: bool = False) -> FlowMemoryCell[T]:
        # noinspection PyProtectedMember
        return self.flow_executor._memory_for_node(self.nid, name, var_type, initial_value, persistent)

    def _register_provider(self, provider: TNodeInput[Any]) -> None:
        from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode

        if isinstance(provider, FlowSingleOutputNode):
            provider.setup()
            provider.to(self.flow_executor.var(f"_tmp.{random_string(10)}", provider.get_type()))
