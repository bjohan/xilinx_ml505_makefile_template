from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence

from component_axi4s_head_unpacker import axi4s_head_unpacker
dataToWrite =  [    0xA0, 0xA1, 0xA2, 0xC0, 0xA3, 0xB0, 0xC0, 0x03,  0xB1,          0xB0, 0xB1, 0xB2, 0x03, 0xC0, 0xC0,             0xC0, 0xC1, 0xC2, 0xC0, 0x03, 0xE3,     0xD0, 0xD1, 0xD2, 0xC0,     0xFF,       0xE0, 0xE1, 0xE2]
writeDelays  = [    0,    3,    0,    0,    1,    0,    0,    0,     1,             0,    0,    4,    0,    0,    0,                0,    0,    0,    0,    0,    2,        0,    0,    0,    0,        0,          0,    0,    0]
writeLast   =  [    0,    0,    0,    0,    0,    0,    0,    0,     1,             0,    0,    0,    0,    0,    1,                0,    0,    0,    0,    0,    1,        0,    0,    0,    1,        1,          0,    0,    1]

dataToRead = [      0xA2A1A0,                                                       0xB2B1B0,                                       0xC2C1C0,                               0xD2D1D0,                   0x0000FF,   0xE2E1E0]
readDelays = [      0,                                                              0,                                              10,                                     0,                          3,          0]

tailReadData = [                      0xC0, 0xA3, 0xB0, 0xC0, 0x03, 0xB1,                             0x03, 0xc0, 0xc0,                              0xc0, 0x03, 0xe3,                      0xC0]
tailReadDelays  = [                   1,    0,    0,    0,    1,    0,                                 0,    4,    0,                                0,    0,    0,                         2]
tailReadLast =    [                   0,    0,    0,    0,    0,    1,                                 0,    0,    1,                                0,    0,    1,                         1]

@block
def test_axi4s_head_unpacker():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   

    tailDone = Signal(False)

    tail_out = Axi4sInterface(8);
    i = Axi4sInterface(8);
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    outRegs = Signal(intbv(0)[8*3:])

    nWords = Signal(intbv(0, min = 0, max = 8))

    valid = Signal(False)
    ready = Signal(False)
    axi4s_unpacker_inst = axi4s_head_unpacker(reset, clk, i, tail_out, outRegs, valid, ready, nWords)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge


    @instance
    def monitor():
        for i in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");


    @instance
    def read_tail():
        yield reset.negedge; 
        yield tbReceiveSequence(clk, tail_out, tailReadData, tailReadLast, tailReadDelays)
        tailDone.next = 1


    @instance
    def read():
        yield reset.negedge;
        tail_out.ready.next = 1
        yield clk.posedge
        ready.next = 0
        for data, delay in zip(dataToRead, readDelays):
            for j in range(delay):
                yield clk.posedge
            ready.next = 1
            yield clk.posedge
            while not valid:
                yield clk.posedge
            if data != outRegs:
                print("Output does not match. Expected", data, "got:", outRegs)
                quit(-1)
            print("Output:", outRegs) 
            ready.next = 0
        while not tailDone:
            yield clk.posedge
        for i in range(10):
            yield clk.posedge
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge; 
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays)

    return clkgen,  gen_reset, axi4s_unpacker_inst, write, read, monitor, read_tail

tb = test_axi4s_head_unpacker();
tb.config_sim(trace=True)
tb.run_sim();
