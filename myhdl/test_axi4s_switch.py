from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence


from component_axi4s_switch import axi4s_switch

dataToWrite = [  0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                            0xB0, 0xB1, 0xB2,     0xC0, 0xC1,                      0xd0, 0xe0, 0xf0, 0xdd]
writeDelays = [  0,    0,    1,    0,    0,                               4,    0,    0,        0,    0,                         0,    0,    0,    0]
writeLast   = [  0,    0,    0,    0,    1,                               0,    0,    1,        0,    1,                         1,    1,    1,    1]

dataToReadA = [  0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                                                  0xC0, 0xC1,                            0xe0,       0xdd]
readDelaysA = [  0,    0,    1,    1,    1,                                                     0,    1,                               0,          0]
readLastA   = [  0,    0,    0,    0,    1,                                                     0,    1,                               1,          1]

dataToReadB = [                                                           0xB0, 0xB1, 0xB2,                                      0xd0,        0xf0]
readDelaysB = [                                                           4,    0,    0,                                         0,           0]
readLastB   = [                                                           0,    0,    1,                                         1,           1]

muxAStates =  [  1,                                                       0,                    1,                               0,     1,    0,     1]

@block
def test_axi4s_switch():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8)
    oa = Axi4sInterface(8) 
    ob = Axi4sInterface(8)
    
    toA = Signal(False)
    toB = Signal(False)

    axi4s_switch_inst = axi4s_switch(reset, clk, i, oa, ob, toA, toB)

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
    def read_a():
        yield reset.negedge
        yield tbReceiveSequence(clk, oa, dataToReadA, readLastA, readDelaysA);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def read_b():
        yield reset.negedge
        yield tbReceiveSequence(clk, ob, dataToReadB, readLastB, readDelaysB);


    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, dataToWrite, writeLast, writeDelays);


    @instance
    def mux_control():
        yield reset.negedge
        for s in muxAStates:
            toA.next = s
            toB.next = not s
            yield clk.posedge
            while True:
                if i.ready and i.valid and i.last:
                    break
                else:
                    yield clk.posedge

    return gen_reset, clkgen, axi4s_switch_inst, write, read_a, read_b, monitor, mux_control

tb = test_axi4s_switch();
tb.config_sim(trace=True)
tb.run_sim();
