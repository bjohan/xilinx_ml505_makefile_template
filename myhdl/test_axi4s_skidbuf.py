from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_skidbuf import axi4s_skidbuf

@block
def test_axi4s_skidbuf():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    i = Axi4sInterface(8); 
    o = Axi4sInterface(8);
 
    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    axi4s_skidbuf_inst = axi4s_skidbuf(reset, clk, i, o)

    @instance
    def monitor():
        for nclk in range(100):
            yield clk.posedge
        raise StopSimulation("Too many clk cycles elapsed, increase nclk if needed")

    @instance
    def read():
        for j in range(3):
            yield clk.posedge
        o.ready.next = 1
        while True:
            if not o.valid:
                yield o.valid.posedge
            yield clk.posedge
            o.ready.next = 0;
            yield clk.posedge
            o.ready.next = 1;

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        print("Waiting 3 clks")
        for j in range(3):
            yield clk.posedge
        print("Starting to transmit")
        yield clk.posedge
        for b in [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]:
            i.valid.next = 1
            i.data.next = b
            if b in [0xA3, 0xB3, 0xC3]:
                i.last.next = 1
            else:
                i.last.next = 0
            yield clk.negedge
            if not i.ready:
                yield i.ready.posedge
            yield clk.posedge
            i.valid.next = 1
        print("extra clocks")
        for j in range(3):
            yield clk.posedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, axi4s_skidbuf_inst, write, read, monitor

tb = test_axi4s_skidbuf();
tb.config_sim(trace=True)
tb.run_sim();
