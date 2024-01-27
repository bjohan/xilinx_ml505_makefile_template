from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_address_switch import axi4s_address_switch

dataToWrite = [   0x1,  0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                            0xB0, 0xB1, 0xB2,    0xFF, 0xF0, 0xF1, 0xF2,    0x01, 0xC0, 0xC1,                      0xd0]
writeDelays = [   0,    0,    0,    1,    0,    0,                               4,    0,    0,       0,    0,    0,    0,       0,    0,    0,                         0]
writeLast   = [   0,    0,    0,    0,    0,    1,                               0,    0,    1,       0,    0,    0,    1,       0,    0,    1,                         1]

dataToReadM = [        0xA0, 0xA1, 0xA2, 0xA3, 0xA4,                                                  0xFF, 0xF0, 0xF1, 0xF2,    0xC0, 0xC1,                      ]
readDelaysM = [        0,    0,    1,    1,    1,                                                     1,    1,    0,    1,       0,    1,                         ]
readLastM   = [        0,    0,    0,    0,    1,                                                     0,    0,    0,    1,       0,    1,                         ]

dataToReadO = [                                                                 0xB0, 0xB1, 0xB2,     0xff, 0xF0, 0xF1, 0xF2,                                          0xd0]
readDelaysO = [                                                                 4,    0,    0,        0,    0,    0,    0,                                             0]
readLastO   = [                                                                 0,    0,    1,        0,    0,    0,    1,                                             1]

@block
def test_axi4s_address_switch():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8)
    o = Axi4sInterface(8) 
    om = Axi4sInterface(8)
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    transferIn = Signal(False)
    transferOut = Signal(False)
    lastOutMarker = Signal(False)
    tick = Signal(False)
    readRef = Signal(intbv(0)[8:])

    axi4s_address_switch_inst = axi4s_address_switch(reset, clk,
        i, om, 0x01, o )

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
    def read_bypass():
        yield reset.negedge;
        yield clk.posedge
        for data, last, delay in zip(dataToReadO, readLastO, readDelaysO):
            lastOutMarker.next = last
            readRef.next = data
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
        #raise StopSimulation("Simulation stopped")

    @instance
    def read_address_switch():
        yield reset.negedge;
        yield clk.posedge
        for data, last, delay in zip(dataToReadM, readLastM, readDelaysM):
            lastOutMarker.next = last
            readRef.next = data
            om.ready.next = 0
            for j in range(delay):
                yield clk.posedge
            om.ready.next = 1
            yield clk.posedge
            while not om.transacts():
                yield clk.posedge
            print("Mux Received", om.data, " referece value ", intbv(data), " result:", om.data == data)
            if last:
                print()
        om.ready.next = 0;
        #raise StopSimulation("Simulation stopped")


    @instance
    def write():
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        
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
        i.valid.next = 0
        for j in range(3):
            yield clk.posedge

    return clkgen, axi4s_address_switch_inst, write, read_bypass, read_address_switch, monitor

tb = test_axi4s_address_switch();
tb.config_sim(trace=True)
tb.run_sim();
