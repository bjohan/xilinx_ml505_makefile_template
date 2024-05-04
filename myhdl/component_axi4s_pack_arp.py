from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_packer import axi4s_packer

@block
def axi4s_pack_arp(reset, clk, o, hardware_type, protocol_type, hardware_size, protocol_size, opcode, sender_mac, sender_ip, target_mac, target_ip, valid, ready):
   
    numWords = Signal(intbv(0)[16:])
    header = Signal(modbv(0)[8*(2+2+1+1+2+2*(6+4)):])
    #txOne = Signal(False)
    axi4s_packer_inst = axi4s_packer(reset, clk, o, header, valid ,ready, False)

    @always_comb
    def comb():
        header.next[16:0] = hardware_type
        header.next[32:16] = protocol_type
        header.next[40:32] = hardware_size
        header.next[48:40] = protocol_size
        header.next[64:48] = opcode
        header.next[112:64] = sender_mac
        header.next[144:112] = sender_ip
        header.next[192:144] = target_mac
        header.next[224:192] = target_ip

    return comb, axi4s_packer_inst
