from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_last_deescaper import axi4s_last_deescaper

dataToRead = [0xFF,                       0xA0, 0xA1, 0xC0, 0xA3, 0xB0, 0xB1,                             0xB2, 0xB3, 0xC0,                                       0xC0, 0xE2,             0xE3,                      0xc0]
readDelays = [0,                          0,    0,    0,    1,    0,    0,                                4,    0,    0,                                          0,    0,                0,                        0]
readLast   = [1,                          0,    0,    0,    0,    0,    1,                                0,    0,    1,                                          0,    0,                1,                        1]
dataToWrite =  [0xC0, 0x03, 0xFF,         0xA0, 0xA1, 0xC0, 0xC0, 0xA3, 0xB0, 0xC0, 0x03,  0xB1,          0xB2, 0xB3, 0xC0, 0x03, 0xC0, 0xC0,             0xC0, 0xC0, 0xE2, 0xC0, 0x03, 0xE3,   0xC0, 0x3, 0xC0, 0xC0]
writeDelays  = [13,    13,    13,            0,    3,    0,    0,    1,    0,    0,    0,     1,             0,    0,    4,    0,    0,    0,                0,    0,    0,    0,    0,    2,      0,    0,   0,    0]
writeLast   =  [0,    0,    0,            0,    0,    0,    0,    0,    0,    0,    0,     1,             0,    0,    0,    0,    0,    1,                0,    0,    0,    0,    0,    1,      0,    0,   0,    1]
@block
def test_axi4s_last_deescaper():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
  
    i = Axi4sInterface(8);
    o = Axi4sInterface(8); 
    frameError = Signal(False)

    axi4s_last_deescaper_inst = axi4s_last_deescaper(reset, clk, i, o, frameError, 0xc0, 0x03)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(100):
            yield clk.posedge
        print("Simulation did not end successfully")
        quit(-1)

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    @instance
    def read():
        yield reset.negedge
        yield tbReceiveSequence(clk, o, dataToRead, readLast, readDelays);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays);


    return clkgen, gen_reset, monitor, axi4s_last_deescaper_inst, write, read



    return clkgen,  axi4s_last_deescaper_inst, write, read, monitor

tb = test_axi4s_last_deescaper();
tb.config_sim(trace=True)
tb.run_sim();
