from datetime import timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.flow_value import FlowVariable
from pycontrolflow.FlowTimer import FlowTimer


class FlowTimerRepeating(FlowTimer):
    def __init__(self, flow_executor: FlowExecutor, name: str, interval: timedelta) -> None:
        super().__init__(name)
        self.interval = interval

        self._timer = timedelta()
        self.elapsed = FlowVariable(name + ".elapsed", bool, False)

    def start_cycle(self) -> None:
        self.elapsed.set(False)

    def process(self, delta: timedelta) -> None:
        self._timer += delta

        if self._timer > self.interval:
            self.elapsed.set(True)
            self._timer = timedelta()
