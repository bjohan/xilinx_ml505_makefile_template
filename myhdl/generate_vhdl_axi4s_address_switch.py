from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_address_switch import axi4s_address_switch

def convert_axi4s_address_switch(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8);
    om = Axi4sInterface(8); 
    o = Axi4sInterface(8); 
    axi4s_address_switch_inst = axi4s_address_switch(reset, clk, i, om, 0x01, o)
    axi4s_address_switch_inst.convert(hdl=hdl);


convert_axi4s_address_switch(hdl='VHDL')
