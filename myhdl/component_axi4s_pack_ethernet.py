from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_prepender import axi4s_prepender
from component_axi4s_pad_to_length import axi4s_pad_to_length
from component_axi4s_ethernet_fcs_generator import axi4s_ethernet_fcs_generator
from component_axi4s_appender import axi4s_appender

@block
def axi4s_pack_ethernet(reset, clk, i, o, sfd, dst, src, etherType, valid, ready):
   
    numWords = Signal(intbv(0)[16:])
    header = Signal(modbv(0)[8*(1+2*6+2):])

    padded = Axi4sInterface(8)
    withHeader = Axi4sInterface(8)
    withHeader2 = Axi4sInterface(8)

    padding = Signal(modbv(0)[8:])
    fcs = Signal(modbv(0)[32:])

    axi4s_pad_to_length_inst = axi4s_pad_to_length(reset, clk, i, padded, 46, padding)
    axi4s_prepender_inst = axi4s_prepender(reset, clk, padded, withHeader, header)
    axi4s_ethernet_fcs_generator_inst = axi4s_ethernet_fcs_generator(reset, clk, withHeader, withHeader2, fcs)
    axi4s_appender_inst = axi4s_appender(reset, clk, withHeader2, o, fcs)

    @always_comb
    def comb():
        header.next[8:0] = sfd.next
        header.next[56:8] = dst.next
        header.next[104:56] = src.next
        header.next[120:104] = etherType.next

    return comb, axi4s_prepender_inst, axi4s_pad_to_length_inst, axi4s_ethernet_fcs_generator_inst, axi4s_appender_inst
