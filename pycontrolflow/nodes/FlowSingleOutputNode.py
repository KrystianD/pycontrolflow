import typing
from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Any, Type, Sequence

from pycontrolflow import type_utils
from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.FlowNode import FlowNode

TFlowSingleOutputNodeType = TypeVar("TFlowSingleOutputNodeType")


class FlowSingleOutputNode(FlowNode, IFlowValueProvider[TFlowSingleOutputNodeType], typing.Generic[TFlowSingleOutputNodeType], ABC):
    def __init__(self, providers: Sequence[IFlowValueProvider[Any]], nid: Optional[str] = None) -> None:
        super().__init__(providers, nid=nid)
        self.output_value: Optional[FlowValue[TFlowSingleOutputNodeType]] = None

    def to(self, output_value: FlowValue[TFlowSingleOutputNodeType]) -> 'FlowSingleOutputNode[TFlowSingleOutputNodeType]':
        node_type = self._get_output_type()
        output_value_type = output_value.get_type()

        if output_value_type != node_type:
            raise TypeError(f"output type does not match expected type, got: {output_value_type}, expected: {node_type}")
        self.output_value = output_value
        return self

    def set_output(self, value: TFlowSingleOutputNodeType) -> None:
        assert self.output_value is not None
        self.output_value.set(value)

    def get(self) -> Optional[TFlowSingleOutputNodeType]:
        assert self.output_value is not None
        return self.output_value.get()

    # noinspection PyUnresolvedReferences
    # noinspection PyProtectedMember
    def get_type(self) -> Type[TFlowSingleOutputNodeType]:
        if hasattr(self, "__orig_class__"):
            return typing.get_args(getattr(self, "__orig_class__"))[0]  # type: ignore
        for v in self.__orig_bases__:  # type: ignore
            if isinstance(v, typing._GenericAlias):  # type: ignore
                return typing.get_args(v)[0]  # type: ignore
        assert False

    def _get_output_type(self):
        return type_utils.get_generic_args_for_obj(self, FlowSingleOutputNode)[0]
