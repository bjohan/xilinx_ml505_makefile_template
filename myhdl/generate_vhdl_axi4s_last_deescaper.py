from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_last_deescaper import axi4s_last_deescaper

def convert_axi4s_last_deescaper(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8, withLast = False);
    o = Axi4sInterface(8); 
    frameError = Signal(False)
    axi4s_last_deescaper_inst = axi4s_last_deescaper(reset, clk, i, o, frameError, 0xC0, 0x03)
    axi4s_last_deescaper_inst.convert(hdl=hdl);


convert_axi4s_last_deescaper(hdl='VHDL')
