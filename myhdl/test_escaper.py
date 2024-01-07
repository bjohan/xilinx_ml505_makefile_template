from myhdl import *


from component_escaper import escaper

dataToTransfer = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
writeDelays =    [0,    0,    0,    1,    0,    0,    4,    0,    0,    0,    0,    0]
writeLast   =    [0,    0,    0,    0,    0,    1,    0,    0,    1,    0,    0,    0]
readDelays  =    [0,    1,    0,    1,    0,    0,    4,    0,    0,    0,    2,    1]
@block
def test_escaper():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    transferIn = Signal(False)
    transferOut = Signal(False)
    tick = Signal(False)

    escaper_inst = escaper(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn, 
        tDataOut, tValidOut, tReadyIn, tLastOut,
        0xC0)

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
    @instance
    def monitor():
        for i in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");


    @instance
    def read():
        yield reset.negedge;
        for data, last, delay in zip(dataToTransfer, writeLast, readDelays):
            tReadyIn.next = 0
            for i in range(delay):
                yield clk.negedge
            tReadyIn.next = 1
            if not tValidOut:
                yield tValidOut.posedge
            yield clk.posedge
            print("Received", tDataOut, " referece value ", intbv(data), " last was: ", tLastOut, " should be", last)
        tReadyIn.next = 0;

    @instance
    def write():
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = 0
        for i in range(3):
            yield clk.posedge
        
        for data, last, delay in zip(dataToTransfer, writeLast, writeDelays):
            tValidIn.next = 0
            tDataIn.next = data
            tLastIn.next = last
            for i in range(delay):
                yield clk.posedge
            yield clk.negedge
            tValidIn.next = 1
            if not transferIn:
                tick.next = 1
                yield transferIn.posedge
                tick.next = 0
                #yield clk.negedge
            yield clk.posedge
        for i in range(3):
            yield clk.negedge
        raise StopSimulation("Simulation stopped")

    return clkgen, transfer_logic, escaper_inst, write, read, monitor

tb = test_escaper();
tb.config_sim(trace=True)
tb.run_sim();
