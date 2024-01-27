from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_address_merge import axi4s_address_merge

dataToThrough = [   0x1,  0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                                             0xAA, 0xAB, 0xAC]
throughDelays = [   0,    0,    0,    1,    0,    0,                                                4,    0,    0,  ]
throughLast   = [   0,    0,    0,    0,    0,    1,                                                0,    0,    1,  ]

dataToMerge = [                                                    0xB0, 0xB1, 0xB2, 0xB3, 0xB4,                                0xBA, 0xBB, 0xBC]
mergeDelays = [                                                    10,   0,    0,     1,    0,                                  4,    0,    0,  ]
mergeLast   = [                                                    0,    0,    0,     0,    1,                                  0,    0,    1,  ]

dataToRead = [      0x01, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4,      0x02, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4,    0xAA, 0xAB, 0xAC,     0x02, 0xBA, 0xBB, 0xBC]
readDelays = [      0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    0,       1,    0,    0,        0,    1,    1,    0,  ]
readLast   = [      0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    1,       0,    0,    1,        0,    0,    0,    1,  ]

@block
def test_axi4s_address_merge():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    through = Axi4sInterface(8)
    merge = Axi4sInterface(8)
    o = Axi4sInterface(8) 
    writeWait = Signal(False)
    writeBlocked = Signal(False)

    axi4s_address_merge_inst = axi4s_address_merge(reset, clk,
        through, merge, 0x02, o )

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
            o.ready.next = 0
            for j in range(delay):
                yield clk.posedge
            o.ready.next = 1
            yield clk.posedge
            while not o.transacts():
                yield clk.posedge
            print("Out Received", o.data, " referece value ", intbv(data), " result:", o.data == data)
            if last:
                print()
        o.ready.next = 0;

    @instance
    def write_through():
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        
        for data, last, delay in zip(dataToThrough, throughLast, throughDelays):
            through.valid.next = 0
            through.data.next = data
            through.last.next = last
            writeWait.next = 1
            for j in range(delay):
                yield clk.posedge
            writeWait.next = 0
            through.valid.next = 1
            yield clk.posedge
            writeBlocked.next = 1
            while not through.transacts():
                yield clk.posedge
            writeBlocked.next = 0
        through.valid.next = 0
        for j in range(3):
            yield clk.posedge

    @instance
    def write_merge():
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        
        for data, last, delay in zip(dataToMerge, mergeLast, mergeDelays):
            merge.valid.next = 0
            merge.data.next = data
            merge.last.next = last
            writeWait.next = 1
            for j in range(delay):
                yield clk.posedge
            writeWait.next = 0
            merge.valid.next = 1
            yield clk.posedge
            writeBlocked.next = 1
            while not merge.transacts():
                yield clk.posedge
            writeBlocked.next = 0
        merge.valid.next = 0
        for j in range(3):
            yield clk.posedge


    return clkgen, axi4s_address_merge_inst, write_through, read_out, write_merge, monitor

tb = test_axi4s_address_merge();
tb.config_sim(trace=True)
tb.run_sim();
