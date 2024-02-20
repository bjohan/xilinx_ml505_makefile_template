from myhdl import *

from component_configurable_trigger import configurable_trigger
@block
def test_configurable_trigger():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    dataIn = Signal(modbv(0)[4:])
    compare = Signal(modbv(0)[4:])
    care = Signal(modbv(0)[4:])
    trigged = Signal(False)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    configurable_trigger_inst = configurable_trigger(reset, clk, dataIn, compare, care, trigged)

    @instance
    def monitor():
        for nclk in range(100):
            yield clk.posedge
        raise StopSimulation("Too many clk cycles elapsed, increase nclk if needed")

    @instance
    def write():
        reset.next = 1
        for i in range(3):
            yield clk.posedge

        reset.next = 0
        compare.next = 0b0001
        care.next = 0b0111

        for i in range(3):
            yield clk.posedge

        for b in range(16):
            dataIn.next = b
            yield clk.posedge

        for i in range(3):
            yield clk.posedge

        raise StopSimulation("Simulation stopped")

    return clkgen, configurable_trigger_inst, write, monitor

tb = test_configurable_trigger();
tb.config_sim(trace=True)
tb.run_sim();
