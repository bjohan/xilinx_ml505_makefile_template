from myhdl import *
from component_ram import ram

def convert_ram(hdl):
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    address = Signal(intbv(0)[8:])
    we = Signal(False)
    nWords = 16;
    ram_inst = ram(reset, clk, din, dout, address, we, nWords)
    ram_inst.convert(hdl=hdl);

convert_ram(hdl='VHDL')
