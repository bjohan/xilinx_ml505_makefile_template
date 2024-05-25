from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_head_unpacker import axi4s_head_unpacker
from component_axi4s_prepender import axi4s_prepender

@block
def axi4s_unpack_ethernet(reset, clk, i, o, sfd, dst, src, etherType, valid, ready):
  
    etherTyper = Signal(modbv(0)[16:]) 
    numWords = Signal(intbv(0)[16:])
    header = Signal(modbv(0)[8*(1+2*6+2):])

    axi4s_head_unpacker_inst = axi4s_head_unpacker(reset, clk, i, o, header, valid, ready, numWords)

    @always_comb
    def comb():
        sfd.next = header[8:0]
        dst.next = header[56:8]
        src.next = header[104:56]
        etherType.next = header[120:104]
        etherTyper.next = header[120:104]

    return comb, axi4s_head_unpacker_inst
