from myhdl import *
from interface_axi4s import Axi4sInterface


from component_test_application_str import test_application_str

dataToWrite = [   0xFF,                                            0x01, 0xAB, 0xAC]
writeDelays = [   0,                                                4,    0,    0,  ]
writeLast   = [   1,                                                0,    0,    1,  ]

dataToRead = [      0x01, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4,      0x02, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4,    0xAA, 0xAB, 0xAC,     0x02, 0xBA, 0xBB, 0xBC]
readDelays = [      0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    0,       1,    0,    0,        0,    1,    1,    0,  ]
readLast   = [      0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    1,       0,    0,    1,        0,    0,    0,    1,  ]

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
        for j in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");


    @instance
    def read_out():
        yield reset.negedge;
        yield clk.posedge
        for data, last, delay in zip(dataToRead, readLast, readDelays):
            streamOut.ready.next = 0
            for j in range(delay):
                yield clk.posedge
            streamOut.ready.next = 1
            yield clk.posedge
            while not streamOut.transacts():
                yield clk.posedge
            print("Out Received", streamOut.data, " referece value ", intbv(data), " result:", streamOut.data == data)
            if last:
                print()
        streamOut.ready.next = 0;

    @instance
    def write():
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        
        for data, last, delay in zip(dataToWrite, writeLast, writeDelays):
            streamIn.valid.next = 0
            streamIn.data.next = data
            streamIn.last.next = last
            for j in range(delay):
                yield clk.posedge
            streamIn.valid.next = 1
            yield clk.posedge
            while not streamIn.transacts():
                yield clk.posedge
        streamIn.valid.next = 0
        for j in range(3):
            yield clk.posedge

    return clkgen, test_application_str_inst, write, read_out, monitor

tb = test_test_application_str();
tb.config_sim(trace=True)
tb.run_sim();
