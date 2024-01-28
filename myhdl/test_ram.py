from myhdl import *
from component_ram import ram

@block
def test_ram():
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    address = Signal(intbv(0)[8:])
    we = Signal(False)
    nWords = 16;
    ram_inst = ram(reset, clk, din, dout, address, we, nWords)

    @always(delay(10))
    def clkgen():
        clk.next = not clk


    @instance
    def stimulus():
        print("reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = False
        for i in range(3):
            yield clk.posedge

        print("Starting to generate pattern")
        for a in range(nWords):
            address.next = a;
            din.next = nWords-a-1;
            we.next = 1
            yield clk.posedge

        for a in range(nWords):
            address.next = a
            we.next = 0
            yield clk.posedge
            if dout != nWords-a-1:
                print("address", a, "does not match. was:", dout, "should be", nWords-a-1)

        
        raise StopSimulation("Simulation stopped")

    return clkgen, ram_inst, stimulus

tb = test_ram();
tb.config_sim(trace=True)
tb.run_sim();
#traceSignals.name = "test_rs232tx"
#t = traceSignals(test_rs232tx)
#sim = Simulation(t)
#sim.run()
