from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_merge import axi4s_merge

def convert_axi4s_merge(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    a = Axi4sInterface(8)
    b = Axi4sInterface(8)
    o = Axi4sInterface(8) 

    axi4s_merge_inst = axi4s_merge(reset, clk, a, b, o )

    axi4s_merge_inst.convert(hdl=hdl);


convert_axi4s_merge(hdl='VHDL')
