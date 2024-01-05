from myhdl import *


from component_axi4sn import axi4sn

def convert_axi4sn(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[32:])
    tValidIn = Signal(False);
    tReadyOut = Signal(False);
    tLastIn = Signal(False);
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False);
    tLastOut = Signal(False);


    axi4sn_inst = axi4sn(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, 4)
    axi4sn_inst.convert(hdl=hdl);


convert_axi4sn(hdl='VHDL')
