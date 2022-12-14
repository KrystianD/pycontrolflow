from datetime import datetime, timedelta
from typing import Dict, Any, List, Type, TypeVar, Optional, Union, TYPE_CHECKING

from pycontrolflow.Flow import Flow
from pycontrolflow.FlowTimer import FlowTimer
from pycontrolflow.date_utils import parse_timedelta
from pycontrolflow.flow_value import FlowValue, FlowVariable, FlowMemoryCell
from pycontrolflow.nodes.FlowNode import FlowNode
from pycontrolflow.string_utils import random_string

if TYPE_CHECKING:
    from pycontrolflow.FlowTimerOneShot import FlowTimerOneShot
    from pycontrolflow.FlowTimerRepeating import FlowTimerRepeating

T = TypeVar("T")

TState = Dict[str, Union[str, float, None]]


class FlowExecutor:
    def __init__(self) -> None:
        self._flow = Flow()
        self._values: Dict[str, FlowValue[Any]] = {}
        self._timers: Dict[str, FlowTimer] = {}

        self._prev_timestamp: Optional[datetime] = None

        self._is_executing = False

    def set_value(self, name: str, value: Any) -> None:
        self._values[name].set(value)

    def get_value(self, name: str) -> Any:
        return self._values[name].get()

    def serialize_state(self) -> TState:
        state = {}
        for cell in self._values.values():
            if isinstance(cell, FlowMemoryCell) and cell.persistent:
                state[cell.name] = cell.to_json()
        return state

    def from_state(self, state: Optional[TState]) -> None:
        if state is None:
            return
        for cell in self._values.values():
            if isinstance(cell, FlowMemoryCell) and cell.persistent:
                if cell.name in state:
                    cell.from_json(state[cell.name])

    def add(self, items: List[FlowNode]) -> None:
        self._flow.append(items)
        self._flow.set_executor(self)
        self._flow.setup()

    def run(self, timestamp: datetime) -> None:
        if self._prev_timestamp is None:
            self._prev_timestamp = timestamp
        delta = timestamp - self._prev_timestamp
        self._prev_timestamp = timestamp

        try:
            self._is_executing = True

            # start new cycle
            for item in self._values.values():
                if isinstance(item, FlowVariable):
                    item.start_cycle()
            for timer in self._timers.values():
                timer.start_cycle()

            # process timers
            for timer in self._timers.values():
                timer.process(delta)

            # process lines
            for line in self._flow.items:
                line.process(timestamp, delta)

            # process timers after
            for timer in self._timers.values():
                timer.process_after()
        finally:
            self._is_executing = False

    def reset_state(self) -> None:
        for line in self._flow.items:
            line.reset_state()

    def memory(self, name: str, var_type: Type[T], initial_value: T, persistent: bool = False) -> FlowMemoryCell[T]:
        obj = FlowMemoryCell(self, name, var_type, initial_value, persistent=persistent)
        self._values[name] = obj
        return obj

    def var(self, name: str, var_type: Type[T], default: Optional[T] = None) -> FlowVariable[T]:
        obj = FlowVariable(self, name, var_type, default if default is not None else var_type())
        self._values[name] = obj
        return obj

    def timer_one_shot(self, name: str, duration: Union[str, timedelta], extend_on_trigger: bool) -> 'FlowTimerOneShot':
        from pycontrolflow.FlowTimerOneShot import FlowTimerOneShot
        obj = FlowTimerOneShot(self, name, parse_timedelta(duration), extend_on_trigger)
        self._timers[name] = obj
        return obj

    def timer_repeating(self, name: str, interval: Union[str, timedelta]) -> 'FlowTimerRepeating':
        from pycontrolflow.FlowTimerRepeating import FlowTimerRepeating
        obj = FlowTimerRepeating(self, name, parse_timedelta(interval))
        self._timers[name] = obj
        return obj

    def _var_for_node(self, nid: Optional[str], name: str, var_type: Type[T], default: Any = None) -> FlowVariable[T]:
        path = f"_tmp_node.{random_string(10)}.{name}"
        return self.var(path, var_type, default)

    def _memory_for_node(self, nid: Optional[str], name: str, var_type: Type[T], initial_value: T,
                         persistent: bool = False) -> FlowMemoryCell[T]:
        if persistent:
            if nid is None:
                raise Exception("can't create persistent memory cell without node id (nid)")
            path = f"_node.{nid}.{name}"
        else:
            path = f"_tmp_node.{random_string(10)}.{name}"
        return self.memory(path, var_type, initial_value, persistent)
