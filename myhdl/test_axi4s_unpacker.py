from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_unpacker import axi4s_unpacker
dataToWrite =  [   0xA0, 0xA1, 0xA2, 0xC0, 0xA3, 0xB0, 0xC0, 0x03,  0xB1,          0xB0, 0xB1, 0xB2, 0x03, 0xC0, 0xC0,             0xC0, 0xC1, 0xC2, 0xC0, 0x03, 0xE3,   0xD0, 0xD1, 0xD2, 0xC0]
writeDelays  = [   0,    3,    0,    0,    1,    0,    0,    0,     1,             0,    0,    4,    0,    0,    0,                0,    0,    0,    0,    0,    2,      0,    0,   0,    0]
writeLast   =  [   0,    0,    0,    0,    0,    0,    0,    0,     1,             0,    0,    0,    0,    0,    1,                0,    0,    0,    0,    0,    1,      0,    0,   0,    1]

dataToRead = [0xA2A1A0, 0xB2B1B0, 0xC2C2C0, 0xD2D1D0]
readDelays = [0, 0, 10, 0]

@block
def test_axi4s_unpacker():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    i = Axi4sInterface(8);
    i.ready.next = 1
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    outRegs = Signal(intbv(0)[8*3:])


    valid = Signal(False)
    ready = Signal(False)
    axi4s_unpacker_inst = axi4s_unpacker(reset, clk, i, outRegs, 8, valid, ready )

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
        ready.next = 0
        for data, delay in zip(dataToRead, readDelays):
            for j in range(delay):
                yield clk.posedge
            ready.next = 1
            yield clk.posedge
            while not valid:
                yield clk.posedge
            print("Output:", outRegs) 
            ready.next = 0

    @instance
    def write():
        outRegs.next = 0 
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        #outRegs.set(0,0)
        for data, last, delay in zip(dataToWrite, writeLast, writeDelays):
            i.valid.next = 0
            i.data.next = data
            i.last.next = last 
            writeWait.next = 1
            for j in range(delay):
                yield clk.posedge
            writeWait.next = 0
            i.valid.next = 1
            yield clk.posedge
            writeBlocked.next = 1
            while not i.transacts():
                yield clk.posedge
            writeBlocked.next = 0
        for j in range(3):
            yield clk.posedge

    return clkgen,  axi4s_unpacker_inst, write, read, monitor

tb = test_axi4s_unpacker();
tb.config_sim(trace=True)
tb.run_sim();
