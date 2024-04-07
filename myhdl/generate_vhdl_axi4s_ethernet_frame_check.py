from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_ethernet_frame_check import axi4s_ethernet_frame_check

def convert_axi4s_ethernet_frame_check(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    valid = Signal(False)
    framed = Axi4sInterface(8); 
    checked = Axi4sInterface(8); 

    axi4s_ethernet_frame_check_inst = axi4s_ethernet_frame_check(reset, clk,framed, checked, valid)
    axi4s_ethernet_frame_check_inst.convert(hdl=hdl);


convert_axi4s_ethernet_frame_check(hdl='VHDL')
