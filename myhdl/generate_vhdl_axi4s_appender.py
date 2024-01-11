from myhdl import *

from component_axi4s_appender import axi4s_appender

def convert_axi4s_appender(hdl):
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

    axi4s_appender_inst = axi4s_appender(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, Signal(intbv(0x0210)[16:]))
    axi4s_appender_inst.convert(hdl=hdl);


convert_axi4s_appender(hdl='VHDL')
