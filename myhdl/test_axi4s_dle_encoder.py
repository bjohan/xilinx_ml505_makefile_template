from myhdl import *

from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_dle_encoder import axi4s_dle_encoder

dataToWrite = [               0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1,                               0xB2, 0xB3, 0xC0,                               0xC1, 0xC2, 0xC3]
writeDelays =    [            0,    0,    0,    1,    0,    0,                                  4,    0,    0,                                  0,    0,    0]
writeLast   =    [            0,    0,    0,    0,    0,    1,                                  0,    0,    1,                                  0,    0,    1]
dataToRead =  [   0xC0, 0x02, 0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xC0, 0x03,       0xC0, 0x02, 0xB2, 0xB3, 0xC0, 0xC0, 0xC0, 0x03,       0xC0, 0x02, 0xC1, 0xC2, 0xC3, 0xC0, 0x03]
readDelays  = [   0,    0,    0,    3,    0,    1,    0,    1,    0,    0,          0,    0,    0,    0,    4,    0,    0,    0,          0,    0,    0,    0,    0,    2,    1]
readLast   =  [   0,    0,    0,    0,    0,    0,    0,    0,    0,    1,          0,    0,    0,    0,    0,    0,    0,    1,          0,    0,    0,    0,    0,    0,    1]

@block
def test_axi4s_dle_encoder():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)

    i = Axi4sInterface(8) 
    o = Axi4sInterface(8) 

    axi4s_dle_encoder_inst = axi4s_dle_encoder(reset, clk, i, o,) 

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def gen_reset():
        reset.next = 1
        for j in range(3):
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
        yield tbReceiveSequence(clk, o, dataToRead, readLast, readDelays)
        raise StopSimulation("All data correctly received. Simulation stopped.")

    @instance
    def write():
        yield reset.negedge;
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays)

    return clkgen, gen_reset, axi4s_dle_encoder_inst, write, read, monitor

tb = test_axi4s_dle_encoder();
tb.config_sim(trace=True)
tb.run_sim();
