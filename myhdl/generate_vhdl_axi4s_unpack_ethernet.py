from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_unpack_ethernet import axi4s_unpack_ethernet

def convert_axi4s_unpack_ethernet(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    valids = Axi4sInterface(8);
    payload = Axi4sInterface(8);

    sfd = Signal(modbv(0)[8:])
    dst = Signal(modbv(0)[48:])
    src = Signal(modbv(0)[48:])
    etherType = Signal(modbv(0)[16:])

    headerValid = Signal(True)
    headerReady = Signal(True)


    axi4s_unpack_ethernet_inst = axi4s_unpack_ethernet(reset, clk, valids, payload, sfd, dst, src, etherType, headerValid, headerReady)

    axi4s_unpack_ethernet_inst.convert(hdl=hdl);


convert_axi4s_unpack_ethernet(hdl='VHDL')
