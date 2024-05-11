from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_truncate_to_length import axi4s_truncate_to_length

def convert_axi4s_truncate_to_length(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    i = Axi4sInterface(8)
    o = Axi4sInterface(8)
  
    minimumLength = Signal(modbv(5)[32:])
    axi4s_truncate_to_length_inst = axi4s_truncate_to_length(reset, clk, i, o, minimumLength)
    axi4s_truncate_to_length_inst.convert(hdl=hdl);


convert_axi4s_truncate_to_length(hdl='VHDL')
