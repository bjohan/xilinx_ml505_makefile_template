from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_test_application_str import test_application_str

dataToWrite = [   0xFF,                                            0x01, 0xAB, 0xAC]
writeDelays = [   0,                                               4,    0,    0,  ]
writeLast   = [   1,                                               0,    0,    1,  ]

dataToRead = [    0xFF, 0x01, 0xFF,                                0x01, 0xAB, 0xAC]
readDelays = [    0,    0,    0,                                   0,    0,    0]
readLast   = [    1,    0,    1,                                   0,    0,    1]

@block
def test_test_application_str():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    streamIn = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 

    test_application_str_inst = test_application_str(reset, clk, streamIn, streamOut )

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
        yield tbReceiveSequence(clk, streamOut, dataToRead, readLast, readDelays);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, streamIn, dataToWrite, writeLast, writeDelays);


    return clkgen, gen_reset, monitor, test_application_str_inst, write, read

tb = test_test_application_str();
tb.config_sim(trace=True)
tb.run_sim();
