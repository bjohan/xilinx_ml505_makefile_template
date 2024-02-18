from myhdl import *
from component_rs232rx import rs232rx
from interface_axi4s import Axi4sInterface

def convert_rs232rx(hdl):
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    o = Axi4sInterface(8, withLast=False)
    txd = Signal(True)
    baudDiv = Signal(intbv(min=0, max=2**24))
    rs232rx_inst = rs232rx(reset, clk, o, txd, baudDiv);
    rs232rx_inst.convert(hdl=hdl);


convert_rs232rx(hdl='VHDL')
