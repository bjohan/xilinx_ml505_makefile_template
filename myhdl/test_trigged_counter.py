from myhdl import *
from component_trigged_counter import trigged_counter

@block
def test_trigged_counter():
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    counter = Signal(intbv(0)[8:])
    count = Signal(False)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    trigged_counter_inst = trigged_counter(reset, clk, count, counter)

    @instance
    def stimulus():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = False
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.negedge
        print("Starting to generate pattern")
        for a in range(512):
            count.next = True
            for i in range(10):
                yield clk.negedge
                count.next = False
        raise StopSimulation("Simulation stopped")

    return clkgen, trigged_counter_inst, stimulus

tb = test_trigged_counter();
tb.config_sim(trace=True)
tb.run_sim();
#traceSignals.name = "test_rs232tx"
#t = traceSignals(test_rs232tx)
#sim = Simulation(t)
#sim.run()
