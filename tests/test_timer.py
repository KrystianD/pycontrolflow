import unittest
from datetime import datetime, timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.timers.TriggerTimer import TriggerTimer
from pycontrolflow.nodes.flow_control.If import If
from pycontrolflow.nodes.values.Move import Move


class TimerTest(unittest.TestCase):
    def test_basic(self):
        executor = FlowExecutor()

        var1 = executor.memory("var1", bool, initial_value=False)
        t1 = executor.timer_one_shot("t1", "10s", extend_on_trigger=False)

        executor.add([
            Move(var1, t1.trigger),
            # If(var1, [
            #     TriggerTimer(t1),
            # ])
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 0))
        self.assertFalse(t1.enabled.get())

        var1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 5))
        self.assertTrue(t1.enabled.get())

        var1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 10))
        self.assertTrue(t1.enabled.get())
        self.assertEqual(timedelta(seconds=5), t1.timer.get())

        executor.run(datetime(2020, 1, 1, 15, 0, 15))
        self.assertFalse(t1.enabled.get())
        self.assertEqual(timedelta(seconds=10), t1.timer.get())

        executor.run(datetime(2020, 1, 1, 15, 0, 30))
        self.assertFalse(t1.enabled.get())
        self.assertEqual(timedelta(seconds=10), t1.timer.get())

    def test_extend(self):
        executor = FlowExecutor()

        var1 = executor.memory("var1", bool, initial_value=False)
        t1 = executor.timer_one_shot("t1", "10s", extend_on_trigger=True)

        executor.add([
            Move(var1, t1.trigger),
            # If(var1, [
            #     TriggerTimer(t1),
            # ])
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 0))
        self.assertFalse(t1.enabled.get())

        var1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 5))
        self.assertTrue(t1.enabled.get())

        var1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 10))
        self.assertTrue(t1.enabled.get())
        self.assertEqual(timedelta(seconds=5), t1.timer.get())

        var1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 15))
        self.assertTrue(t1.enabled.get())
        self.assertEqual(timedelta(seconds=0), t1.timer.get())
        var1.set(False)

        executor.run(datetime(2020, 1, 1, 15, 0, 20))
        self.assertTrue(t1.enabled.get())
        self.assertEqual(timedelta(seconds=5), t1.timer.get())

        executor.run(datetime(2020, 1, 1, 15, 0, 30))
        self.assertFalse(t1.enabled.get())
        self.assertEqual(timedelta(seconds=10), t1.timer.get())


if __name__ == '__main__':
    unittest.main()
