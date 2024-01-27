from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_address_merge import axi4s_address_merge

def convert_axi4s_address_merge(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    t = Axi4sInterface(8);
    m = Axi4sInterface(8); 
    o = Axi4sInterface(8); 
    axi4s_address_merge_inst = axi4s_address_merge(reset, clk, t, m, 0x01, o)
    axi4s_address_merge_inst.convert(hdl=hdl);


convert_axi4s_address_merge(hdl='VHDL')
