from abc import abstractmethod
from datetime import timedelta


class FlowTimer:
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def start_cycle(self) -> None:
        pass

    @abstractmethod
    def process(self, delta: timedelta) -> None:
        pass

    @abstractmethod
    def process_after(self) -> None:
        pass
