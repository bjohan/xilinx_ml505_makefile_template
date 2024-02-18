from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_last_escaper import axi4s_last_escaper

dataToWrite = [0xFF,               0xA0, 0xA1, 0xC0, 0xA3, 0xB0, 0xB1,                             0xB2, 0xB3, 0xC0,                               0xC0, 0xC2, 0xC3,                      0xc0]
writeDelays = [0,                  0,    0,    0,    1,    0,    0,                                4,    0,    0,                                  0,    0,    0,                        0]
writeLast   = [1,                  0,    0,    0,    0,    0,    1,                                0,    0,    1,                                  0,    0,    1,                        1]
dataToRead =  [0xC0, 0x03, 0xFF,   0xA0, 0xA1, 0xC0, 0xC0, 0xA3, 0xB0, 0xC0, 0x03,  0xB1,          0xB2, 0xB3, 0xC0, 0x03, 0xC0, 0xC0,             0xC0, 0xC0, 0xC2, 0xC0, 0x03, 0xC3,   0xC0, 0x3, 0xC0, 0xC0]
readDelays  = [5,    5,    5,      0,    3,    0,    0,    1,    0,    0,    0,     1,             0,    0,    4,    0,    0,    0,                0,    0,    0,    0,    0,    2,      0,    0,   0,    0]
readLast   =  [0,    0,    1,      0,    0,    0,    0,    0,    0,    0,    0,     1,             0,    0,    0,    0,    0,    1,                0,    0,    0,    0,    0,    1,      0,    0,   0,    1]
@block
def test_axi4s_last_escaper():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8);
    o = Axi4sInterface(8, withLast=False); 

    writeWait = Signal(False)
    writeBlocked = Signal(False)
    
    transferIn = Signal(False)
    transferOut = Signal(False)
    lastOutMarker = Signal(False)
    tick = Signal(False)
    readRef = Signal(intbv(0)[8:])

    axi4s_last_escaper_inst = axi4s_last_escaper(reset, clk,
        i, o,  
        0xc0, 0x03)

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
    def read():
        yield reset.negedge;
        yield clk.posedge
        for data, last, delay in zip(dataToRead, readLast, readDelays):
            lastOutMarker.next = last
            readRef.next = data
            o.ready.next = 0
            for j in range(delay):
                yield clk.posedge
            o.ready.next = 1
            yield clk.posedge
            while not o.transacts():
                print("wai")
                yield clk.posedge
            print("Received", o.data, " referece value ", intbv(data), " result:", o.data == data)
            if last:
                print()
        o.ready.next = 0;
        raise StopSimulation("Simulation stopped")

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
        for j in range(3):
            yield clk.posedge

    return clkgen, axi4s_last_escaper_inst, write, read, monitor

tb = test_axi4s_last_escaper();
tb.config_sim(trace=True)
tb.run_sim();
