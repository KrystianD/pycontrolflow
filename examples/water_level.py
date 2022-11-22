import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.SchmittGate import SchmittGate
from pycontrolflow.nodes.datetime.TimeCheck import TimeCheck
from pycontrolflow.nodes.logic.And import And

ticks = 0


def main():
    executor = FlowExecutor()

    start_date = datetime.datetime(2022, 1, 1, 0, 0, 0)

    water_level = executor.memory("current_level", float, 0)  # Memory cell holding current water level
    pump_required = executor.var("pump_required", bool)  # Variable holding value if water level is too low
    time_check_ok = executor.var("time_check_ok", bool)  # Variable holding value if pump can be enabled
    pump_enabled = executor.var("pump_enabled", bool)  # Output variable determining if pump should be on

    executor.add([
        SchmittGate(water_level, 20, 40, initial=True, invert=True).to(pump_required),
        TimeCheck(datetime.time(0, 0, 0), datetime.time(0, 7, 30)).to(time_check_ok),

        And(pump_required, time_check_ok).to(pump_enabled),
    ])

    animation_end_time = 600
    animation_interval = 0.1

    figure, ax = plt.subplots()
    ax.set_xlim(0, animation_end_time)
    ax.set_ylim(0, 100)
    line, = ax.plot(0, 0)

    x = []
    y = []

    def animation_function(i):
        global ticks

        ticks += 1

        cur_date = start_date + datetime.timedelta(seconds=ticks)
        executor.run(cur_date)

        is_pump_enabled = pump_enabled.get()

        if is_pump_enabled:
            water_level.increment(1.5)

        if water_level.get() > 0:
            water_level.increment(-0.3)

        x.append(i * (1 / animation_interval))
        y.append(water_level.get())

        line.set_xdata(x)
        line.set_ydata(y)
        return line,

    _ = FuncAnimation(figure,
                      func=animation_function,
                      frames=np.arange(0, animation_end_time, animation_interval),
                      interval=1 / animation_interval,
                      repeat=False)
    plt.show()


main()
