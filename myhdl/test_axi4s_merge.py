from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence


from component_axi4s_merge import axi4s_merge

dataToA =    [   0x1,  0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                                             0xAA, 0xAB, 0xAC]
aDelays =    [   0,    0,    0,    1,    0,    0,                                                4,    0,    0,  ]
aLast   =    [   0,    0,    0,    0,    0,    1,                                                0,    0,    1,  ]

dataToB =    [                                                    0xB0, 0xB1, 0xB2, 0xB3, 0xB4,                                0xBA, 0xBB, 0xBC]
bDelays =    [                                                    10,   0,    0,     1,    0,                                  4,    0,    0,  ]
bLast   =    [                                                    0,    0,    0,     0,    1,                                  0,    0,    1,  ]

dataToRead = [      0x01, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4,            0xB0, 0xB1, 0xB2, 0xB3, 0xB4,    0xAA, 0xAB, 0xAC,           0xBA, 0xBB, 0xBC]
readDelays = [      0,    0,    0,    0,    0,    1,               0,    0,    0,    0,    0,       1,    0,    0,              1,    1,    0,  ]
readLast   = [      0,    0,    0,    0,    0,    1,               0,    0,    0,    0,    1,       0,    0,    1,              0,    0,    1,  ]

@block
def test_axi4s_merge():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    a = Axi4sInterface(8)
    b = Axi4sInterface(8)
    o = Axi4sInterface(8) 

    axi4s_merge_inst = axi4s_merge(reset, clk, a, b, o )

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
    def read_out():
        yield reset.negedge;
        yield tbReceiveSequence(clk, o, dataToRead, readLast, readDelays);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write_a():
        yield reset.negedge
        yield tbTransmitSequence(clk, a, dataToA, aLast, aDelays)

    @instance
    def write_b():
        yield reset.negedge
        yield tbTransmitSequence(clk, b, dataToB, bLast, bDelays)


    return clkgen, axi4s_merge_inst, write_a, read_out, write_b, monitor, gen_reset

tb = test_axi4s_merge();
tb.config_sim(trace=True)
tb.run_sim();
