from myhdl import *

from component_deescaper import deescaper

def convert_deescaper(hdl):
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

    deescaper_inst = deescaper(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, 0x10)
    deescaper_inst.convert(hdl=hdl);


convert_deescaper(hdl='VHDL')
