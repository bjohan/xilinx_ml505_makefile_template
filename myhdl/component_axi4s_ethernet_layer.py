from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_receive_ethernet import axi4s_receive_ethernet
from component_axi4s_unpack_ethernet import axi4s_unpack_ethernet
from component_axi4s_prepender import axi4s_prepender

@block
def axi4s_ethernet_layer(reset, clk, rxdata, rxdv, o):
    rxeth = Axi4sInterface(8)
    packetLength = Signal(intbv(0)[16:])

    rxeth_payload = Axi4sInterface(8)

    sfd = Signal(modbv(0)[8:])
    dst = Signal(modbv(0)[48:])
    src = Signal(modbv(0)[48:])
    etherType = Signal(modbv(0)[16:])

    headerValid = Signal(True)
    headerReady = Signal(True)

    packetLength = Signal(intbv(0)[16:])


    #eth_layer = Axi4sInterface(8)

    i_recive_ethernet = axi4s_receive_ethernet(reset, clk, rxdata, rxdv, rxeth, packetLength)
    i_axi4s_unpack_ethernet_inst = axi4s_unpack_ethernet(reset, clk, rxeth, rxeth_payload, sfd, dst, src, etherType, headerValid, headerReady)
    i_axi4s_prepender_inst = axi4s_prepender(reset, clk, rxeth_payload, o, etherType)
    



    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            headerReady.next = True
            #i.ready.next = 1
            #o.valid.next = i.valid
            #o.data.next = i.data
            #o.last.next = i.last
            #if i.valid:
            #    if not first:
            #        csum.next = crcOut
            #        byteCount.next = byteCount+1
            #    else:
            #        first.next = False
            #if i.last:
            #    csum.next = 0xFFFFFFFF
            #    first.next = True
            #    if byteCount > 3:
            #        frameLength.next = byteCount-3
            #    else:
            #        frameLength.next = 0
            #    if crcOut == modbv(0xDEBB20E3)[32:]:
            #        valid.next = True
            #    else:
            #        valid.next = False
        
    return  logic, i_recive_ethernet, i_axi4s_unpack_ethernet_inst, i_axi4s_prepender_inst
