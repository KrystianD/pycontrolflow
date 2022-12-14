import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.util.Select import Select


class Test(unittest.TestCase):
    def test_fixed(self) -> None:
        executor = FlowExecutor()

        cond1 = executor.memory("cond1", bool, initial_value=False)
        cond2 = executor.memory("cond2", bool, initial_value=False)
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

        cond1 = executor.memory("cond1", bool, initial_value=False)
        value1 = executor.memory("value1", int, initial_value=0)
        cond2 = executor.memory("cond2", bool, initial_value=False)
        value2 = executor.memory("value2", int, initial_value=0)
        value_def = executor.memory("value_def", int, initial_value=0)
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
