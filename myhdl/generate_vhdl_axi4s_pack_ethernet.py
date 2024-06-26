from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_pack_ethernet import axi4s_pack_ethernet

def convert_axi4s_pack_ethernet(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    valids = Axi4sInterface(8);
    payload = Axi4sInterface(8);

    sfd = Signal(modbv(0)[8:])
    dst = Signal(modbv(0)[48:])
    src = Signal(modbv(0)[48:])

    headerValid = Signal(True)
    headerReady = Signal(True)


    axi4s_pack_ethernet_inst = axi4s_pack_ethernet(reset, clk, valids, payload, sfd, dst, src, headerValid, headerReady)

    axi4s_pack_ethernet_inst.convert(hdl=hdl);


convert_axi4s_pack_ethernet(hdl='VHDL')
