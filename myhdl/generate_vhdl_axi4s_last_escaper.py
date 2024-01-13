from myhdl import *

from component_axi4s_last_escaper import axi4s_last_escaper

def convert_axi4s_last_escaper(hdl):
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

    axi4s_last_escaper_inst = axi4s_last_escaper(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, 0xC0, 0x03)
    axi4s_last_escaper_inst.convert(hdl=hdl);


convert_axi4s_last_escaper(hdl='VHDL')
