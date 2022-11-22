import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.values.Move import Move


class MoveTest(unittest.TestCase):
    def test_value(self) -> None:
        executor = FlowExecutor()

        var1 = executor.memory("var1", int, initial_value=0)

        executor.add([
            Move(2, var1),
        ])

        executor.run(datetime.now())
        self.assertEqual(2, var1.get())

    def test_reg(self) -> None:
        executor = FlowExecutor()

        var1 = executor.memory("var1", int, initial_value=0)
        var2 = executor.memory("var2", int, initial_value=0)

        executor.add([
            Move[int](var1, var2),
        ])

        var1.set(5)
        var2.set(6)

        self.assertEqual(5, var1.get())
        self.assertEqual(6, var2.get())
        executor.run(datetime.now())
        self.assertEqual(5, var1.get())
        self.assertEqual(5, var2.get())
