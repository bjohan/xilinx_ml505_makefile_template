from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_last_escaper import axi4s_last_escaper

def convert_axi4s_last_escaper(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8);
    o = Axi4sInterface(8, withLast=False); 
    axi4s_last_escaper_inst = axi4s_last_escaper(reset, clk, i, o, 0xC0, 0x03)
    axi4s_last_escaper_inst.convert(hdl=hdl);


convert_axi4s_last_escaper(hdl='VHDL')
