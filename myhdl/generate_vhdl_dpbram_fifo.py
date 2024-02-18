from myhdl import *
from component_dpbram_fifo import dpbram_fifo

def convert_dpbram_fifo(hdl):

    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[32:])
    dout = Signal(intbv(0)[32:])
    we = Signal(False)
    ready = Signal(False)
    valid = Signal(False)
    re = Signal(False)
    new = Signal(False)
    empty = Signal(False)
    nWords = 1024;
    dpbram_fifo_inst = dpbram_fifo(reset, clk, din, we, ready, dout, re, valid, empty, new, nWords)
    dpbram_fifo_inst.convert(hdl=hdl);

convert_dpbram_fifo(hdl='VHDL')
