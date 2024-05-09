from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_switch import axi4s_switch

def convert_axi4s_switch(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8)
    oa = Axi4sInterface(8) 
    ob = Axi4sInterface(8)
    
    toA = Signal(False)
    toB = Signal(False)

    axi4s_switch_inst = axi4s_switch(reset, clk, i, oa, ob, toA, toB)

    axi4s_switch_inst.convert(hdl=hdl);


convert_axi4s_switch(hdl='VHDL')
