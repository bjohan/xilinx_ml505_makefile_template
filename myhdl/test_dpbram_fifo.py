from myhdl import *
from component_dpbram_fifo import dpbram_fifo

@block
def test_dpbram_fifo():
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    wref = Signal(intbv(0)[8:])
    rref = Signal(intbv(0)[8:])
    we = Signal(False)
    re = Signal(False)
    ready = Signal(False)
    valid = Signal(False)
    empty = Signal(False)
    new = Signal(False)
    
    nWords = 16;
    dpbram_fifo_inst = dpbram_fifo(reset, clk, din,we, ready, dout, re, valid, empty, new, nWords)
    @always(delay(10))
    def clkgen():
        clk.next = not clk
    
    @instance
    def monitor():
        for j in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");


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
        for a in range(nWords+30):
            we.next = 1
            din.next = a+100;
            yield clk.posedge
            while not ready:
                yield clk.posedge
            wref.next = a
            we.next = 0

    @instance
    def compare():
        for a in range(nWords+30):
            while not new:
                yield clk.posedge
            if int(dout) != int(a+100):
                print("data", int(a+100), "does not match. was:", int(dout))
            else:
                print("data", int(a+100), "does MATCH. was:", int(dout))
            yield clk.posedge

    @instance
    def stimulus_read():
        print("reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = False
        for i in range(40):
            yield clk.posedge
        for a in range(nWords+30):
            re.next = 1
            yield clk.posedge
            while not valid:
                yield clk.posedge
            re.next = 0
            if a == 40:
                for q in range(4):
                    yield clk.posedge
            #yield clk.posedge

        
        raise StopSimulation("Simulation stopped")

    return clkgen, monitor, dpbram_fifo_inst, stimulus_write, stimulus_read, compare

tb = test_dpbram_fifo();
tb.config_sim(trace=True)
tb.run_sim();
#traceSignals.name = "test_rs232tx"
#t = traceSignals(test_rs232tx)
#sim = Simulation(t)
#sim.run()
