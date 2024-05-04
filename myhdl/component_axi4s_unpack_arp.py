from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_head_unpacker import axi4s_head_unpacker

@block
def axi4s_unpack_arp(reset, clk, i, o, hardware_type, protocol_type, hardware_size, protocol_size, opcode, sender_mac, sender_ip, target_mac, target_ip, valid, ready):
   
    numWords = Signal(intbv(0)[16:])
    header = Signal(modbv(0)[8*(2+2+1+1+2+2*(6+4)):])

    axi4s_head_unpacker_inst = axi4s_head_unpacker(reset, clk, i, o, header, valid, ready, numWords)

    @always_comb
    def comb():
        hardware_type.next = header[16:0]
        protocol_type.next = header[32:16]
        hardware_size.next = header[40:32]
        protocol_size.next = header[48:40]
        opcode.next = header[64:48]
        sender_mac.next = header[112:64]
        sender_ip.next = header[144:112]
        target_mac.next = header[192:144]
        target_ip.next = header[224:192]

    return comb, axi4s_head_unpacker_inst
