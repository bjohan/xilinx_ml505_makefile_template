from myhdl import *

from interface_axi4s import Axi4sInterface

from component_axi4s_skidbuf import axi4s_skidbuf
from component_axi4s_last_deescaper import axi4s_last_deescaper
from component_axi4s_last_escaper import axi4s_last_escaper

dataToRead = [   0xA0, 0xA1, 0xC0, 0xA3, 0xB0, 0xB1,                             0xB2, 0xB3, 0xC0,                                       0xC0, 0xE2,             0xE3,                      0xc0,     0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xa5, 0xa6, 0xa7, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf]
readDelays = [   0,    0,    0,    0,    0,    0,                                0,    0,    0,                                          0,    0,                0,                        0,          0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,   0]
readLast   = [   0,    0,    0,    0,    0,    1,                                0,    0,    1,                                          0,    0,                1,                        1,          0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1]

dataToWrite = dataToRead
writeDelays = readDelays
writeLast = readLast

@block
def simulation_axi4s_escaping():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    i = Axi4sInterface(8);
    isk = Axi4sInterface(8);
    c = Axi4sInterface(8); 
    csk = Axi4sInterface(8); 
    o = Axi4sInterface(8); 
    osk = Axi4sInterface(8); 

    writeWait = Signal(False)
    writeBlocked = Signal(False)

   
    
    lastOutMarker = Signal(False)
    readRef = Signal(intbv(0)[8:])

    frameError = Signal(False)

    readMark = Signal(False)

    axi4s_isk = axi4s_skidbuf(reset, clk, i, isk)
    axi4s_last_escaper_inst = axi4s_last_escaper(reset, clk, 
        isk, c,
        0xc0, 0x03)

    axi4s_csk = axi4s_skidbuf(reset, clk, c, csk)
    axi4s_last_deescaper_inst = axi4s_last_deescaper(reset, clk, 
        csk, o,  
        frameError, 0xc0, 0x03)
    axi4s_osk = axi4s_skidbuf(reset, clk, o, osk)

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
            osk.ready.next = 0
            for j in range(delay):
                yield clk.posedge
            osk.ready.next = 1
            readMark.next = 1
            yield clk.posedge
            while not osk.transacts():
                yield clk.posedge
            print("Received", osk.data, " referece value ", intbv(data), " result:", osk.data == data, "Last correct: ", last == osk.last)
            readMark.next = 0
            if last:
                print()
        osk.ready.next = 0;
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

    return clkgen, axi4s_isk, axi4s_osk, axi4s_csk, axi4s_last_deescaper_inst, axi4s_last_escaper_inst, write, read, monitor

tb = simulation_axi4s_escaping();
tb.config_sim(trace=True)
tb.run_sim();
