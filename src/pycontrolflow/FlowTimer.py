from abc import abstractmethod
from datetime import timedelta, datetime


class FlowTimer:
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def start_cycle(self) -> None:
        pass

    @abstractmethod
    def process(self, cur_date: datetime, delta: timedelta) -> None:
        pass

    @abstractmethod
    def process_after(self) -> None:
        pass
