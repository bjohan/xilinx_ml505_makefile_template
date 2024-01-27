from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_prepender import axi4s_prepender

def convert_axi4s_prepender(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8);    
    o = Axi4sInterface(8);    
    axi4s_prepender_inst = axi4s_prepender(reset, clk, i,o, Signal(intbv(0x0210)[16:]))
    axi4s_prepender_inst.convert(hdl=hdl);


convert_axi4s_prepender(hdl='VHDL')
