import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.util.Transform import Transform


class TransformTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var1 = executor.memory("var1", int)
        var2 = executor.memory("var2", int)
        out = executor.var("out", int)

        executor.add([
            Transform[int](lambda vals: sum(x.get() for x in vals), var1, var2).to(out),
        ])

        var1.set(1)
        var2.set(2)
        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertEqual(3, out.get())


if __name__ == '__main__':
    unittest.main()
