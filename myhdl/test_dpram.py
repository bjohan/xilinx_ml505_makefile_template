from myhdl import *
from component_dpram import dpram

@block
def test_dpram():
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    raddr = Signal(intbv(0)[8:])
    waddr = Signal(intbv(0)[8:])
    we = Signal(False)
    nWords = 16;
    dpram_inst = dpram(reset, clk, din, waddr, dout, raddr, we, nWords)

    @always(delay(10))
    def clkgen():
        clk.next = not clk


    @instance
    def stimulus_write():
        print("reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = False
        for i in range(3):
            yield clk.posedge

        print("Starting to generate pattern")
        for a in range(nWords):
            waddr.next = a;
            din.next = nWords-a-1;
            we.next = 1
            yield clk.posedge
        we.next = 0

    @instance
    def stimulus_read():
        print("reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = False
        for i in range(6):
            yield clk.posedge
        for a in range(nWords):
            raddr.next = a
            yield clk.posedge
            if dout != nWords-a-1:
                print("address", a, "does not match. was:", dout, "should be", nWords-a-1)

        
        raise StopSimulation("Simulation stopped")

    return clkgen, dpram_inst, stimulus_write, stimulus_read

tb = test_dpram();
tb.config_sim(trace=True)
tb.run_sim();
