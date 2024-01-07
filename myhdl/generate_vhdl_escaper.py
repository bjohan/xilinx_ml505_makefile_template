from myhdl import *

from component_escaper import escaper

def convert_escaper(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    escaper_inst = escaper(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, 0x10)
    escaper_inst.convert(hdl=hdl);


convert_escaper(hdl='VHDL')
