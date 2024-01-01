from myhdl import *


from component_axi4sn import axi4sn

def convert_axi4sn(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[8:])
    tValidIn = Signal(False);
    tReadyOut = Signal(False);
    
    tDataOut = Signal(intbv(0)[32:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False);


    axi4sn_inst = axi4sn(reset, clk, tDataIn, tValidIn, tReadyOut, tDataOut, tValidOut, tReadyIn, 4)
    axi4sn_inst.convert(hdl=hdl);


convert_axi4sn(hdl='VHDL')
