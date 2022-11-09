import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.Changed import Changed


def main():
    executor = FlowExecutor()

    var_in = executor.memory("in", int, initial_value=0)
    var_out = executor.var("out", bool)

    executor.add([
        Changed[int](var_in).to(var_out),
    ])

    var_in.set(1)
    executor.run(datetime.datetime.utcnow())
    print(var_out.get())

    var_in.set(1)
    executor.run(datetime.datetime.utcnow())
    print(var_out.get())

    var_in.set(2)
    executor.run(datetime.datetime.utcnow())
    print(var_out.get())


main()
