import datetime
import unittest

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.logic.And import And
from pycontrolflow.nodes.values.Move import Move


class AndTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var1 = executor.memory("var1", bool, initial_value=False)
        var2 = executor.memory("var2", bool, initial_value=False)
        var3 = executor.memory("var3", bool, initial_value=False)

        executor.add([
            Move(And(var1, var2), var3),
        ])

        executor.run(datetime.datetime.min)
