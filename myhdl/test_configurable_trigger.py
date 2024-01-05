from myhdl import *


from component_configurable_trigger import configurable_trigger
@block
def test_configurable_trigger():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    dataIn = Signal(modbv(0)[4:])
    andMask = Signal(modbv(0)[4:])
    orMask = Signal(modbv(0)[4:])
    trigAnd = Signal(False)
    trigOr = Signal(False)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    configurable_trigger_inst = configurable_trigger(dataIn, andMask, orMask, trigAnd, trigOr)

    @instance
    def monitor():
        for nclk in range(100):
            yield clk.posedge
        raise StopSimulation("Too many clk cycles elapsed, increase nclk if needed")

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        andMask.next = 0b0101
        orMask.next = 0b1010
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.posedge
        print("Starting to transmit")
        yield clk.posedge
        for b in range(16):
            dataIn.next = b
            yield clk.negedge
        print("extra clocks")
        for i in range(3):
            yield clk.posedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, configurable_trigger_inst, write, monitor

tb = test_configurable_trigger();
tb.config_sim(trace=True)
tb.run_sim();
