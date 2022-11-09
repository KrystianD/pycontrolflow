import unittest
from datetime import datetime, timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.timers.TriggerTimer import TriggerTimer
from pycontrolflow.nodes.flow_control.If import If
from pycontrolflow.nodes.values.Move import Move


class MoveTest(unittest.TestCase):
    def test_value(self):
        executor = FlowExecutor()

        var1 = executor.memory("var1", int)

        executor.add([
            Move(2, var1),
        ])

        executor.run(datetime.now())
        self.assertEquals(2, var1.get())

    def test_reg(self):
        executor = FlowExecutor()

        var1 = executor.memory("var1", int)
        var2 = executor.memory("var2", int)

        executor.add([
            Move(var1, var2),
        ])

        var1.set(5)
        var2.set(6)

        self.assertEquals(5, var1.get())
        self.assertEquals(6, var2.get())
        executor.run(datetime.now())
        self.assertEquals(5, var1.get())
        self.assertEquals(5, var2.get())


if __name__ == '__main__':
    unittest.main()
