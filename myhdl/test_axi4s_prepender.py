from myhdl import *

from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_prepender import axi4s_prepender



dataToWrite = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,                               0xB2, 0xB3, 0xC0,                   0xC1, 0xC2,                  0xe0,                 0xf0]
writeDelays =    [0,    0,    0,    1,    0,    0,                               4,    0,    0,                      0,    0,                     0,                    0]
writeLast   =    [0,    0,    0,    0,    0,    1,                               0,    0,    1,                      0,    1,                     1,                    1]
dataToRead =  [0xD0, 0xD1, 0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,       0xD0, 0xD1, 0xB2, 0xB3, 0xC0,       0xD0, 0xD1, 0xC1, 0xC2,      0xD0, 0xD1, 0xe0,     0xD0, 0xD1, 0xF0]
readDelays  = [0,    3,    0,    1,    0,    1,    0,    0,          0,    0,    4,    0,    0,          0,    0,    0,    2,         0,    0,    0,        0,    0,    0]
readLast   =  [0,    0,    0,    0,    0,    0,    0,    1,          0,    0,    0,    0,    1,          0,    0,    0,    1,         0,    0,    1,        0,    0,    1]
@block
def test_axi4s_prepender():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8);    
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    o = Axi4sInterface(8);    
    transferIn = Signal(False)
    transferOut = Signal(False)

    tick = Signal(False)
    readRef = Signal(intbv(0)[8:])

    prependData = Signal(intbv(0xD1D0)[16:])
    axi4s_prepender_inst = axi4s_prepender(reset, clk, i, o, prependData)

    @always_comb
    def transfer_logic():
        transferIn.next = i.valid ==1 and i.ready == 1
        transferOut.next = o.valid == 1 and o.ready == 1



    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for j in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    @instance
    def read():
        yield reset.negedge;
        yield tbReceiveSequence(clk, o, dataToRead, readLast, readDelays)
        raise StopSimulation("Simulation ended successfully. All data received");
        #yield clk.posedge
        #for data, last, delay in zip(dataToRead, readLast, readDelays):
        #    readRef.next = data
        #    o.ready.next = 0
        #    for j in range(delay):
        #        yield clk.posedge
        #    o.ready.next = 1
        #    yield clk.posedge
        #    while not transferOut:
        #        yield clk.posedge
        #    print("Received", i.data, " referece value ", intbv(data), " last was: ", o.last, " should be", last, " result:", o.data == data and o.last==last)
        #    if last:
        #        print()
        #o.ready.next = 0;

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays)
        #reset.next = 1
        #for j in range(3):
        #    yield clk.posedge
        #reset.next = 0
        #for j in range(3):
        #    yield clk.posedge
        #
        #for data, last, delay in zip(dataToWrite, writeLast, writeDelays):
        #    i.valid.next = 0
        #    i.data.next = data
        #    i.last.next = last
        #    writeWait.next = 1
        #    for j in range(delay):
        #        yield clk.posedge
        #    writeWait.next = 0
        #    i.valid.next = 1
        #    yield clk.posedge
        #    writeBlocked.next = 1
        #    while not transferIn:
        #        yield clk.posedge
        #    writeBlocked.next = 0
        #for j in range(3):
        #    yield clk.posedge
        #raise StopSimulation("Simulation stopped")

    return clkgen, transfer_logic, axi4s_prepender_inst, write, read, monitor, gen_reset

tb = test_axi4s_prepender();
tb.config_sim(trace=True)
tb.run_sim();
