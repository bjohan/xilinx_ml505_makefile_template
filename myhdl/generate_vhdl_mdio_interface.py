from myhdl import *
from component_mdio_interface import mdio_interface
from interface_axi4s import Axi4sInterface

def convert_mdio_interface(hdl):
    reset = ResetSignal(0, active=1, isasync=False)
    clk = Signal(False)
    i = Signal(True)
    o = Signal(False)
    t = Signal(False)
    mdc = Signal(False)
    rw = Signal(False)
    phyAddr = Signal(modbv(0)[5:])
    regAddr = Signal(modbv(0)[5:])
    dataWrite = Signal(modbv(0)[16:])
    dataOut = Signal(modbv(0)[16:])
    start = Signal(False)
    busy = Signal(False)
    baudDiv = Signal(intbv(min=0, max=2**24))
        
    mdio_interface_inst = mdio_interface(reset, clk, i, o, t, mdc, rw, phyAddr, regAddr, dataWrite, dataOut, start, busy, baudDiv)
    mdio_interface_inst.convert(hdl=hdl);

convert_mdio_interface(hdl='VHDL')
