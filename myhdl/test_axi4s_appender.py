from myhdl import *

from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_appender import axi4s_appender

dataToWrite = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,                   0xB2, 0xB3, 0xC0,                   0xC1, 0xC2, 0xC3]
writeDelays =    [0,    0,    0,    1,    0,    0,                   4,    0,    0,                      0,    0,    0]
writeLast   =    [0,    0,    0,    0,    0,    1,                   0,    0,    1,                      0,    0,    1]
dataToRead =  [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xD0, 0xD1,       0xB2, 0xB3, 0xC0, 0xD0, 0xD1,       0xC1, 0xC2, 0xC3, 0xD0, 0xD1]
readDelays  = [0,    3,    0,    1,    0,    1,    0,    0,          0,    0,    4,    0,    0,          0,    0,    0,    2,    1]
readLast   =  [0,    0,    0,    0,    0,    0,    0,    1,          0,    0,    0,    0,    1,          0,    0,    0,    0,    1]
@block
def test_axi4s_appender():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8)
    o = Axi4sInterface(8)
  
    prependData = Signal(intbv(0xD1D0)[16:])
    axi4s_appender_inst = axi4s_appender(reset, clk, i, o, prependData)

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
        for j in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");

    @instance
    def read():
        yield reset.negedge;
        yield clk.posedge
        yield tbReceiveSequence(clk, o, dataToRead, readLast, readDelays)
        raise StopSimulation("All data successfully received. Simulation stopped.")

    @instance
    def write():
        yield reset.negedge;
        yield clk.posedge
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays)

    return clkgen, gen_reset, axi4s_appender_inst, write, read, monitor

tb = test_axi4s_appender();
tb.config_sim(trace=True)
tb.run_sim();
