import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.values.Move import Move


class VarTest(unittest.TestCase):
    def test1(self):
        executor = FlowExecutor()

        var1 = executor.var("var1", int)

        executor.add([
            Move(10, var1),
        ])

        executor.run(datetime(2020, 1, 1))

        self.assertEqual(10, var1.get())


if __name__ == '__main__':
    unittest.main()
