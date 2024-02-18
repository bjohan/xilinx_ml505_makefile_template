from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_packer import axi4s_packer


dataToWrite = [0xA2A1A0, 0xB2B1B0, 0xC2C1C0, 0xD2D1D0]
writeDelays = [0, 0, 0, 0]

dataToRead =  [   0xA0, 0xA1, 0xA2,          0xB0, 0xB1, 0xB2,             0xC0,     0xD0, 0xD1, 0xD2]
readDelays  = [   0,    0,    0,             0,    0,    0,                0,        0,    0,    0]
readLast   =  [   0,    0,    1,             0,    0,    1,                1,        0,    0,    1]

@block
def test_axi4s_packer():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    o = Axi4sInterface(8);
    o.ready.next = 1
    writeWait = Signal(False)
    writeBlocked = Signal(False)
    txOne = Signal(False) 
    inRegs = Signal(intbv(0)[8*3:])


    valid = Signal(False)
    ready = Signal(False)
    axi4s_packer_inst = axi4s_packer(reset, clk, o, inRegs, valid, ready, txOne )

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(100):
            yield clk.negedge;
        raise StopSimulation("Ending simulations after 100 cycles");


    @instance
    def read():
        yield reset.negedge;
        yield clk.posedge
        o.ready.next = 0
        for data, last, delay in zip(dataToRead, readLast, readDelays):
            for j in range(delay):
                yield clk.posedge
            o.ready.next = 1
            yield clk.posedge
            while not o.valid:
                yield clk.posedge
            print("Output:", o.data, o.last, data, last)
            if data != o.data or last != o.last:
                print("Output mismatch, simulation failed")
                quit(-1) 
            o.ready.next = 0
        raise StopSimulation("Ending simulation due to sucess");

    @instance
    def write():
        reset.next = 1
        for j in range(3):
            yield clk.posedge
        reset.next = 0
        for j in range(3):
            yield clk.posedge
        #outRegs.set(0,0)
        for data, delay in zip(dataToWrite, writeDelays):
            valid.next = 0
            inRegs.next = data
            writeWait.next = 1
            for j in range(delay):
                yield clk.posedge
            writeWait.next = 0
            valid.next = 1
            if data == 0xC2C1C0:
                txOne.next = 1
            yield clk.posedge
            writeBlocked.next = 1
            while not ready:
                yield clk.posedge
            txOne.next = 0
            writeBlocked.next = 0
        valid.next = 0
        for j in range(3):
            yield clk.posedge

    return clkgen,  axi4s_packer_inst, write, read, monitor

tb = test_axi4s_packer();
tb.config_sim(trace=True)
tb.run_sim();
