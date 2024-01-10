from myhdl import *


from component_axi4s_prepender import axi4s_prepender

dataToWrite = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,                               0xB2, 0xB3, 0xC0,                   0xC1, 0xC2, 0xC3]
writeDelays =    [0,    0,    0,    1,    0,    0,                               4,    0,    0,                      0,    0,    0]
writeLast   =    [0,    0,    0,    0,    0,    1,                               0,    0,    1,                      0,    0,    0]
dataToRead =  [0xD0, 0xD1, 0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,       0xD0, 0xD1, 0xB2, 0xB3, 0xC0,       0xD0, 0xD1, 0xC1, 0xC2, 0xC3]
readDelays  = [0,    3,    0,    1,    0,    1,    0,    0,          0,    0,    4,    0,    0,          0,    0,    0,    2,    1]
readLast   =  [0,    0,    0,    0,    0,    0,    0,    1,          0,    0,    0,    0,    1,          0,    0,    0,    0,    0]
@block
def test_axi4s_prepender():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    transferIn = Signal(False)
    transferOut = Signal(False)
    tick = Signal(False)
    readRef = Signal(intbv(0)[8:])

    prependData = Signal(intbv(0xD1D0)[16:])
    axi4s_prepender_inst = axi4s_prepender(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn, 
        tDataOut, tValidOut, tReadyIn, tLastOut,
        prependData)

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
        yield clk.posedge
        for data, last, delay in zip(dataToRead, readLast, readDelays):
            readRef.next = data
            tReadyIn.next = 0
            for i in range(delay):
                yield clk.posedge
            tReadyIn.next = 1
            yield clk.posedge
            while not transferOut:
                yield clk.posedge
            print("Received", tDataOut, " referece value ", intbv(data), " last was: ", tLastOut, " should be", last, " result:", tDataOut == data and tLastOut==last)
            if last:
                print()
        tReadyIn.next = 0;

    @instance
    def write():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        for i in range(3):
            yield clk.posedge
        
        for data, last, delay in zip(dataToWrite, writeLast, writeDelays):
            tValidIn.next = 0
            tDataIn.next = data
            tLastIn.next = last
            writeWait.next = 1
            for i in range(delay):
                yield clk.posedge
            writeWait.next = 0
            tValidIn.next = 1
            yield clk.posedge
            writeBlocked.next = 1
            while not transferIn:
                yield clk.posedge
            writeBlocked.next = 0
        for i in range(3):
            yield clk.posedge
        raise StopSimulation("Simulation stopped")

    return clkgen, transfer_logic, axi4s_prepender_inst, write, read, monitor

tb = test_axi4s_prepender();
tb.config_sim(trace=True)
tb.run_sim();
