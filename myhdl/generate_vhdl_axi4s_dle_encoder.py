from myhdl import *

from component_axi4s_dle_encoder import axi4s_dle_encoder

def convert_dle_encoder(hdl):
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

    axi4s_dle_encoder_inst = axi4s_dle_encoder(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut)
    axi4s_dle_encoder_inst.convert(hdl=hdl);


convert_dle_encoder(hdl='VHDL')
