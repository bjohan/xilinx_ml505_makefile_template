from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_ethernet_frame_check import axi4s_ethernet_frame_check
from component_axi4s_ethernet_valid_framer import axi4s_ethernet_valid_framer
from component_axi4s_packet_fifo import axi4s_packet_fifo
from component_axi4s_truncate_to_length import axi4s_truncate_to_length

@block
def axi4s_receive_ethernet(reset, clk, rxdata, rx_dv, o, packetLength):
   
    framed = Axi4sInterface(8);
    checked = Axi4sInterface(8);
    buffered = Axi4sInterface(8);
 
    frame_valid = Signal(False)
    frameLength = Signal(intbv(0)[16:])
    packetLengthNoChecksum = Signal(intbv(0)[16:])
    packetLengthr = Signal(intbv(0)[16:])
    discard = Signal(False)

    axi4s_ethernet_valid_framer_inst = axi4s_ethernet_valid_framer(reset, clk, rxdata, rx_dv, framed)
    axi4s_ethernet_frame_check_inst = axi4s_ethernet_frame_check(reset, clk,framed, checked, frame_valid, frameLength)
    axi4s_packet_fifo_inst = axi4s_packet_fifo(reset, clk, checked, discard, buffered, packetLengthr, 2048)
    axi4s_truncate_to_length_inst = axi4s_truncate_to_length(reset, clk, buffered, o, packetLengthNoChecksum)

    @always_comb
    def comb():
        discard.next = (not frame_valid) and checked.last
        packetLength.next = packetLengthr
        if packetLengthr > 4:
            packetLengthNoChecksum.next = packetLengthr-4
        else: 
            packetLengthNoChecksum.next = 0
    

    return comb, axi4s_ethernet_valid_framer_inst, axi4s_ethernet_frame_check_inst, axi4s_packet_fifo_inst, axi4s_truncate_to_length_inst
