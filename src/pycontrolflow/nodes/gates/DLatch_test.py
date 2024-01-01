import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.gates.DLatch import DLatch


class Test(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var_d = executor.memory("var_d", bool, initial_value=False)
        var_e = executor.memory("var_e", bool, initial_value=False)
        var_out = executor.var("out", bool)

        executor.add([
            DLatch[bool](var_d, var_e, initial_state=False).to(var_out)
        ])

        def tick(value: bool, enable: bool, expected_value: bool) -> None:
            var_d.set(value)
            var_e.set(enable)
            executor.run(datetime.now())
            self.assertEqual(expected_value, var_out.get())

        tick(value=True, enable=False, expected_value=False)
        tick(value=True, enable=True, expected_value=True)
        tick(value=True, enable=False, expected_value=True)
        tick(value=False, enable=False, expected_value=True)
        tick(value=False, enable=True, expected_value=False)
        tick(value=False, enable=True, expected_value=False)
        tick(value=False, enable=False, expected_value=False)

        tick(value=False, enable=True, expected_value=False)
        tick(value=True, enable=True, expected_value=True)
        tick(value=False, enable=True, expected_value=False)
