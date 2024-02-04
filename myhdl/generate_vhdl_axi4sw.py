from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4sw import axi4sw

def convert_axi4sw(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    i = Axi4sInterface(8)
    o = Axi4sInterface(32)    

    axi4sw_inst = axi4sw(reset, clk, i, o, 4)
    axi4sw_inst.convert(hdl=hdl);


convert_axi4sw(hdl='VHDL')
