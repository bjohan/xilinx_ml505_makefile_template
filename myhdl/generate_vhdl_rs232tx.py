from myhdl import *
from component_rs232tx import rs232tx
from interface_axi4s import Axi4sInterface

def convert_rs232tx(hdl):
    reset = ResetSignal(0, active=1, isasync=False)
    clk = Signal(False)
    i = Axi4sInterface(8, withLast=False)
    txd = Signal(False)
    baudDiv = Signal(intbv(min=0, max=2**24))

    rs232tx_inst = rs232tx(reset, clk, i, txd, baudDiv)
    rs232tx_inst.convert(hdl=hdl);

convert_rs232tx(hdl='VHDL')
