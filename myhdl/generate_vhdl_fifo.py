from myhdl import *
from component_fifo import fifo

def convert_fifo(hdl):

    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    din = Signal(intbv(0)[8:])
    dout = Signal(intbv(0)[8:])
    we = Signal(False)
    ready = Signal(False)
    valid = Signal(False)
    re = Signal(False)
    nWords = 16;
    fifo_inst = fifo(reset, clk, din, we, ready, dout, re, valid, nWords)
    fifo_inst.convert(hdl=hdl);

convert_fifo(hdl='VHDL')
