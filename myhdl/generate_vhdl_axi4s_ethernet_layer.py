from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_ethernet_layer import axi4s_ethernet_layer

def convert_axi4s_ethernet_layer(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)

    payload = Axi4sInterface(8);

    axi4s_ethernet_layer_inst = axi4s_ethernet_layer(reset, clk, rxdata, rx_dv, payload)

    axi4s_ethernet_layer_inst.convert(hdl=hdl);


convert_axi4s_ethernet_layer(hdl='VHDL')
