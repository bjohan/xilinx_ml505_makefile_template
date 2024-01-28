from myhdl import *
from component_dpram import dpram

def convert_dpram(hdl):

    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    raddr = Signal(intbv(0)[8:])
    waddr = Signal(intbv(0)[8:])
    we = Signal(False)
    nWords = 16;
    dpram_inst = dpram(reset, clk, din, waddr, dout, raddr, we, nWords)
    dpram_inst.convert(hdl=hdl);

convert_dpram(hdl='VHDL')
