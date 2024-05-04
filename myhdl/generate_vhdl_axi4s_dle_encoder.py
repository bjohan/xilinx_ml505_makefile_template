from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_dle_encoder import axi4s_dle_encoder

def convert_dle_encoder(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    i = Axi4sInterface(8) 
    o = Axi4sInterface(8) 

    axi4s_dle_encoder_inst = axi4s_dle_encoder(reset, clk, i, o,) 
    axi4s_dle_encoder_inst.convert(hdl=hdl);


convert_dle_encoder(hdl='VHDL')
