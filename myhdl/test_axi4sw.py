from myhdl import *


from component_axi4sw import axi4sw
@block
def test_axi4sw():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
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

    axi4sw_inst = axi4sw(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, 4)


    @instance
    def read():
        for i in range(3):
            yield clk.negedge
        tReadyIn.next = 1
        yield tValidOut.negedge
        while True:
            if not tValidOut:
                yield tValidOut.posedge
            yield clk.negedge
            yield tValidOut.posedge
            yield tValidOut.negedge
            yield clk.negedge
            tReadyIn.next = 0;

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = 0
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.negedge
        print("Starting to transmit")
        for b in [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]:
            if b == 0xB3:
                tLastIn.next = 1
            else:
                tLastIn.next = 0
            tDataIn.next = b
            if not tReadyOut:
                yield tReadyOut.posedge
            yield clk.negedge
            tValidIn.next = 1
            yield clk.negedge
            tValidIn.next = 0
            #print("Waiting for ack")
            #yield txReady.negedge, delay(30)
            #if txReady:
            #    raise StopSimulation("txValid did not deassert")
        #print("wainting for txready")
        #if not txReady:
        #    yield txReady.posedge
        print("extra clocks")
        for i in range(3):
            yield clk.negedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, transfer_logic, axi4sw_inst, write, read

tb = test_axi4sw();
tb.config_sim(trace=True)
tb.run_sim();
