from myhdl import *


from component_axi4s_skidbuf import axi4s_skidbuf
@block
def test_axi4s_skidbuf():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[32:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)
    
    tDataOut = Signal(intbv(0)[32:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    transferIn = Signal(False)
    transferOut = Signal(False)

    @always_comb
    def transfer_logic():
        transferIn.next = tValidIn ==1 and tReadyOut == 1
        transferOut.next = tValidOut == 1 and tReadyIn == 1

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    axi4s_skidbuf_inst = axi4s_skidbuf(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut)

    @instance
    def monitor():
        for nclk in range(100):
            yield clk.posedge
        raise StopSimulation("Too many clk cycles elapsed, increase nclk if needed")

    @instance
    def read():
        for i in range(3):
            yield clk.posedge
        tReadyIn.next = 1
        #yield tValidOut.negedge
        while True:
            if not tValidOut:
                yield tValidOut.posedge
            yield clk.posedge
            tReadyIn.next = 0;
            #yield tValidOut.posedge
            #yield tValidOut.negedge
            yield clk.posedge
            tReadyIn.next = 1;
            #tReadyIn.next = 0;

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.posedge
        print("Starting to transmit")
        yield clk.posedge
        for b in [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]:
            tValidIn.next = 1
            tDataIn.next = b
            if b in [0xA3, 0xB3, 0xC3]:
                tLastIn.next = 1
            else:
                tLastIn.next = 0
            yield clk.negedge
            if not tReadyOut:
                yield tReadyOut.posedge
            #yield clk.posedge
            yield clk.posedge
            tValidIn.next = 1
            #yield clk.posedge
            #tValidIn.next = 0
            #print("Waiting for ack")
            #yield txReady.negedge, delay(30)
            #if txReady:
            #    raise StopSimulation("txValid did not deassert")
        #print("wainting for txready")
        #if not txReady:
        #    yield txReady.posedge
        print("extra clocks")
        for i in range(3):
            yield clk.posedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, transfer_logic, axi4s_skidbuf_inst, write, read, monitor

tb = test_axi4s_skidbuf();
tb.config_sim(trace=True)
tb.run_sim();
