from myhdl import *


from component_axi4s_skidbuf import axi4s_skidbuf

def convert_axi4s_skidbuf(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[32:])
    tValidIn = Signal(False);
    tReadyOut = Signal(False);
    
    tDataOut = Signal(intbv(0)[32:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False);


    axi4s_skidbuf_inst = axi4s_skidbuf(reset, clk, tDataIn, tValidIn, tReadyOut, tDataOut, tValidOut, tReadyIn)
    axi4s_skidbuf_inst.convert(hdl=hdl);


convert_axi4s_skidbuf(hdl='VHDL')
