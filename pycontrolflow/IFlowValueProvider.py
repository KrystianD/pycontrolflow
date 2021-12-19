from abc import abstractmethod
from typing import Any


class IFlowValueProvider:
    @abstractmethod
    def get(self) -> Any:
        pass
