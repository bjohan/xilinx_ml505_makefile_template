from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_receive_ethernet import axi4s_receive_ethernet

def convert_axi4s_receive_ethernet(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)



    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)

    valids = Axi4sInterface(8);


    packetLength = Signal(intbv(0)[16:])
    axi4s_receive_ethernet_inst = axi4s_receive_ethernet(reset, clk, rxdata, rx_dv, valids, packetLength)

    axi4s_receive_ethernet_inst.convert(hdl=hdl);


convert_axi4s_receive_ethernet(hdl='VHDL')
