from myhdl import *

from component_axi4s_last_deescaper import axi4s_last_deescaper

def convert_axi4s_last_deescaper(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    frameError = Signal(False)
    axi4s_last_deescaper_inst = axi4s_last_deescaper(reset, clk, tDataIn, tValidIn, tReadyOut, tDataOut, tValidOut, tReadyIn, tLastOut, frameError, 0xC0, 0x03)
    axi4s_last_deescaper_inst.convert(hdl=hdl);


convert_axi4s_last_deescaper(hdl='VHDL')
