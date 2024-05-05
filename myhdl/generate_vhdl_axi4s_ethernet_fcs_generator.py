from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_ethernet_fcs_generator import axi4s_ethernet_fcs_generator

def convert_axi4s_ethernet_fcs_generator(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    framed = Axi4sInterface(8); 
    checked = Axi4sInterface(8); 
    fcs = Signal(modbv(0)[32:])

    axi4s_ethernet_fcs_generator_inst = axi4s_ethernet_fcs_generator(reset, clk,framed, checked, fcs)
    axi4s_ethernet_fcs_generator_inst.convert(hdl=hdl);


convert_axi4s_ethernet_fcs_generator(hdl='VHDL')
