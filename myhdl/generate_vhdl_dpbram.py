from myhdl import *
from component_dpbram import dpbram

def convert_dpbram(hdl):
    clk_a = Signal(False)
    wr_a = Signal(False)
    addr_a = Signal(intbv(0)[8:])
    din_a = Signal(intbv(0)[8:])
    dout_a = Signal(intbv(0)[8:])
    
    clk_b = Signal(False)
    wr_b = Signal(False)
    addr_b = Signal(intbv(0)[8:])
    din_b = Signal(intbv(0)[8:])
    dout_b = Signal(intbv(0)[8:])
    
    nWords = 16;
    dpbram_inst = dpbram(clk_a, wr_a, addr_a, din_a, dout_a, clk_b, wr_b, addr_b, din_b, dout_b, nWords)

    dpbram_inst.convert(hdl=hdl);


convert_dpbram(hdl='VHDL')
