from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4sn import axi4sn

def convert_axi4sn(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    i = Axi4sInterface(32)
    o = Axi4sInterface(8)    

    axi4sn_inst = axi4sn(reset, clk, i, o, 4)
    axi4sn_inst.convert(hdl=hdl);


convert_axi4sn(hdl='VHDL')
