import weakref
from typing import Any, Type, Optional, TYPE_CHECKING, TypeVar

from pycontrolflow.flow_value import FlowVariable, FlowMemoryCell
from pycontrolflow.string_utils import random_string

if TYPE_CHECKING:
    from pycontrolflow.FlowExecutor import FlowExecutor

T = TypeVar("T")


def var_for_node(flow_executor: 'FlowExecutor', nid: Optional[str], name: str, var_type: Type[T],
                 default: Any = None, run_on_update: Optional[Any] = None) -> FlowVariable[T]:
    path = f"_tmp_node.{random_string(10)}.{name}"
    var = flow_executor.var(path, var_type, default)

    if run_on_update is not None:
        weak_run_on_update = weakref.ref(run_on_update)

        def fn() -> None:
            run_on_update_ = weak_run_on_update()
            if run_on_update_ is not None:
                run_on_update_.update()

        var.register_on_change(fn)
    return var


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
