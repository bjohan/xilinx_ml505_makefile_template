from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence

from component_mdio_interface import mdio_interface

@block
def test_mdio_interface():
    reset = ResetSignal(0, active=1, isasync=False)
    clk = Signal(False)
    i = Signal(True)
    o = Signal(False)
    t = Signal(False)
    mdc = Signal(False)
    rw = Signal(False)
    phyAddr = Signal(modbv(14)[5:])
    regAddr = Signal(modbv(17)[5:])
    dataWrite = Signal(modbv(0x8001)[16:])
    dataOut = Signal(modbv(0x81)[16:])
    start = Signal(False)
    busy = Signal(False)
        
    mdio_interface_inst = mdio_interface(reset, clk, i, o, t, mdc, rw, phyAddr, regAddr, dataWrite, dataOut, start, busy, 5)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def monitor():
        for i in range(800):
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
    def write():
        yield reset.negedge
        if busy:
            yield busy.negedge
        yield clk.posedge
        rw.next = 0
        start.next = 1
        yield clk.posedge
        start.next = 0
        yield busy.negedge
       
        yield clk.posedge
 
        rw.next = 1
        start.next = 1
        yield clk.posedge
        start.next = 0
        yield busy.negedge
        
        yield clk.posedge
        yield clk.posedge
        raise StopSimulation("Simulation ended successfully")

    return clkgen, gen_reset, monitor, mdio_interface_inst, write

tb = test_mdio_interface();
tb.config_sim(trace=True)
tb.run_sim();
