import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.gates.DLatch import DLatch
from pycontrolflow.nodes.util.Select import Select


class Test(unittest.TestCase):
    def test_fixed(self) -> None:
        executor = FlowExecutor()

        cond1 = executor.memory("cond1", bool)
        cond2 = executor.memory("cond2", bool)
        var_out = executor.var("out", int)

        executor.add([
            Select[int]()
                .case(cond1, 10)
                .case(cond2, 20)
                .default(30)
                .to(var_out)
        ])

        cond1.set(True)
        cond2.set(False)
        executor.run(datetime.now())
        self.assertEqual(10, var_out.get())

        cond1.set(False)
        cond2.set(True)
        executor.run(datetime.now())
        self.assertEqual(20, var_out.get())

        cond1.set(False)
        cond2.set(False)
        executor.run(datetime.now())
        self.assertEqual(30, var_out.get())

    def test_input(self) -> None:
        executor = FlowExecutor()

        cond1 = executor.memory("cond1", bool)
        value1 = executor.memory("value1", int)
        cond2 = executor.memory("cond2", bool)
        value2 = executor.memory("value2", int)
        value_def = executor.memory("value_def", int)
        var_out = executor.var("out", int)

        executor.add([
            Select[int]()
                .case(cond1, value1)
                .case(cond2, value2)
                .default(value_def)
                .to(var_out)
        ])

        value1.set(10)
        value2.set(20)
        value_def.set(30)

        cond1.set(True)
        cond2.set(False)
        executor.run(datetime.now())
        self.assertEqual(10, var_out.get())

        cond1.set(False)
        cond2.set(True)
        executor.run(datetime.now())
        self.assertEqual(20, var_out.get())

        cond1.set(False)
        cond2.set(False)
        executor.run(datetime.now())
        self.assertEqual(30, var_out.get())


if __name__ == '__main__':
    unittest.main()
