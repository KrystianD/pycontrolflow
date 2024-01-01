from typing import Any, Type, Optional, TYPE_CHECKING, TypeVar

from pycontrolflow.flow_value import FlowVariable, FlowMemoryCell
from pycontrolflow.string_utils import random_string

if TYPE_CHECKING:
    from pycontrolflow.FlowExecutor import FlowExecutor

T = TypeVar("T")


def var_for_node(flow_executor: 'FlowExecutor', nid: Optional[str], name: str, var_type: Type[T],
                 default: Any = None) -> FlowVariable[T]:
    path = f"_tmp_node.{random_string(10)}.{name}"
    return flow_executor.var(path, var_type, default)


def memory_for_node(flow_executor: 'FlowExecutor', nid: Optional[str], name: str, var_type: Type[T],
                    initial_value: T,
                    persistent: bool = False) -> FlowMemoryCell[T]:
    if persistent:
        if nid is None:
            raise Exception("can't create persistent memory cell without node id (nid)")
        path = f"_node.{nid}.{name}"
    else:
        path = f"_tmp_node.{random_string(10)}.{name}"
    return flow_executor.memory(path, var_type, initial_value, persistent)
