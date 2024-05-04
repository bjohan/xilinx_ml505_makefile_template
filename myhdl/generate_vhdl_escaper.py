from myhdl import *

from interface_axi4s import Axi4sInterface
from component_escaper import escaper

def convert_escaper(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8)
    o = Axi4sInterface(8)

    escaper_inst = escaper(reset, clk, i, o, 0x10)

    escaper_inst.convert(hdl=hdl);


convert_escaper(hdl='VHDL')
