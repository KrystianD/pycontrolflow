import typing
from abc import ABC
from typing import TypeVar, Generic, Iterable, Optional, Any, Type

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode

TFlowSingleOutputNodeType = TypeVar("TFlowSingleOutputNodeType")


class FlowSingleOutputNode(Generic[TFlowSingleOutputNodeType], FlowNode, IFlowValueProvider[TFlowSingleOutputNodeType], ABC):
    def __init__(self, providers: Optional[Iterable[Any]] = None, nid: Optional[str] = None) -> None:
        super().__init__(providers, nid=nid)
        self.output_value: Optional[FlowValue[TFlowSingleOutputNodeType]] = None

    def to(self, output_value: FlowValue[TFlowSingleOutputNodeType]) -> 'FlowSingleOutputNode[TFlowSingleOutputNodeType]':
        if output_value.get_type() != self.get_type():
            raise TypeError("output type does not match expected type (bool)")
        self.output_value = output_value
        return self

    def set_output(self, value: Any) -> None:
        assert self.output_value is not None
        self.output_value.set(value)

    def get(self) -> Optional[TFlowSingleOutputNodeType]:
        assert self.output_value is not None
        return self.output_value.get()

    def get_type(self) -> Type[TFlowSingleOutputNodeType]:
        for v in self.__orig_bases__:  # type: ignore
            if isinstance(v, typing._GenericAlias):  # type: ignore
                return typing.get_args(v)[0]  # type: ignore
        assert False
