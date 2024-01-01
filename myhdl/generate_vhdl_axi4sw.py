from myhdl import *


from component_axi4sw import axi4sw

def convert_axi4sw(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False);
    tReadyOut = Signal(False);
    
    tDataOut = Signal(intbv(0)[32:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False);


    axi4sw_inst = axi4sw(reset, clk, tDataIn, tValidIn, tReadyOut, tDataOut, tValidOut, tReadyIn, 4)
    axi4sw_inst.convert(hdl=hdl);


convert_axi4sw(hdl='VHDL')
