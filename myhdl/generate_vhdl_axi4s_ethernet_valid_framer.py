from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_ethernet_valid_framer import axi4s_ethernet_valid_framer

def convert_axi4s_ethernet_valid_framer(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)
    o = Axi4sInterface(8); 

    axi4s_ethernet_valid_framer_inst = axi4s_ethernet_valid_framer(reset, clk, rxdata, rx_dv, o)
    axi4s_ethernet_valid_framer_inst.convert(hdl=hdl);


convert_axi4s_ethernet_valid_framer(hdl='VHDL')
