from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_skidbuf import axi4s_skidbuf


#WARNING, does not work for short packets. Intended to be used with ethernet frames which are 64 bytes or longer
@block
def axi4s_ethernet_fcs_generator(reset, clk, i, o, fcs):
    csum = Signal(modbv(0xFFFFFFFF)[32:])
    crcIn = Signal(modbv()[32:])
    crcOut= Signal(modbv()[32:])
    first = Signal(True)
    
    ri = Axi4sInterface(8)
    ro = Axi4sInterface(8)
    axi4s_skidbuf_in_inst = axi4s_skidbuf(reset, clk, i, ri)
    axi4s_skidbuf_out_inst = axi4s_skidbuf(reset, clk, ro, o)

    @always_comb
    def crc_logic():
        crcIn.next = csum
        crcOut.next[0] = crcIn[2] ^ crcIn[8] ^ i.data[2]
        crcOut.next[1] = crcIn[0] ^ crcIn[3] ^ crcIn[9] ^ i.data[0] ^ i.data[3]
        crcOut.next[2] = crcIn[0] ^ crcIn[1] ^ crcIn[4] ^ crcIn[10] ^ i.data[0] ^ i.data[1] ^ i.data[4]
        crcOut.next[3] = crcIn[1] ^ crcIn[2] ^ crcIn[5] ^ crcIn[11] ^ i.data[1] ^ i.data[2] ^ i.data[5]
        crcOut.next[4] = crcIn[0] ^ crcIn[2] ^ crcIn[3] ^ crcIn[6] ^ crcIn[12] ^ i.data[0] ^ i.data[2] ^ i.data[3] ^ i.data[6]
        crcOut.next[5] = crcIn[1] ^ crcIn[3] ^ crcIn[4] ^ crcIn[7] ^ crcIn[13] ^ i.data[1] ^ i.data[3] ^ i.data[4] ^ i.data[7]
        crcOut.next[6] = crcIn[4] ^ crcIn[5] ^ crcIn[14] ^ i.data[4] ^ i.data[5]
        crcOut.next[7] = crcIn[0] ^ crcIn[5] ^ crcIn[6] ^ crcIn[15] ^ i.data[0] ^ i.data[5] ^ i.data[6]
        crcOut.next[8] = crcIn[1] ^ crcIn[6] ^ crcIn[7] ^ crcIn[16] ^ i.data[1] ^ i.data[6] ^ i.data[7]
        crcOut.next[9] = crcIn[7] ^ crcIn[17] ^ i.data[7]
        crcOut.next[10] = crcIn[2] ^ crcIn[18] ^ i.data[2]
        crcOut.next[11] = crcIn[3] ^ crcIn[19] ^ i.data[3]
        crcOut.next[12] = crcIn[0] ^ crcIn[4] ^ crcIn[20] ^ i.data[0] ^ i.data[4]
        crcOut.next[13] = crcIn[0] ^ crcIn[1] ^ crcIn[5] ^ crcIn[21] ^ i.data[0] ^ i.data[1] ^ i.data[5]
        crcOut.next[14] = crcIn[1] ^ crcIn[2] ^ crcIn[6] ^ crcIn[22] ^ i.data[1] ^ i.data[2] ^ i.data[6]
        crcOut.next[15] = crcIn[2] ^ crcIn[3] ^ crcIn[7] ^ crcIn[23] ^ i.data[2] ^ i.data[3] ^ i.data[7]
        crcOut.next[16] = crcIn[0] ^ crcIn[2] ^ crcIn[3] ^ crcIn[4] ^ crcIn[24] ^ i.data[0] ^ i.data[2] ^ i.data[3] ^ i.data[4]
        crcOut.next[17] = crcIn[0] ^ crcIn[1] ^ crcIn[3] ^ crcIn[4] ^ crcIn[5] ^ crcIn[25] ^ i.data[0] ^ i.data[1] ^ i.data[3] ^ i.data[4] ^ i.data[5]
        crcOut.next[18] = crcIn[0] ^ crcIn[1] ^ crcIn[2] ^ crcIn[4] ^ crcIn[5] ^ crcIn[6] ^ crcIn[26] ^ i.data[0] ^ i.data[1] ^ i.data[2] ^ i.data[4] ^ i.data[5] ^ i.data[6]
        crcOut.next[19] = crcIn[1] ^ crcIn[2] ^ crcIn[3] ^ crcIn[5] ^ crcIn[6] ^ crcIn[7] ^ crcIn[27] ^ i.data[1] ^ i.data[2] ^ i.data[3] ^ i.data[5] ^ i.data[6] ^ i.data[7]
        crcOut.next[20] = crcIn[3] ^ crcIn[4] ^ crcIn[6] ^ crcIn[7] ^ crcIn[28] ^ i.data[3] ^ i.data[4] ^ i.data[6] ^ i.data[7]
        crcOut.next[21] = crcIn[2] ^ crcIn[4] ^ crcIn[5] ^ crcIn[7] ^ crcIn[29] ^ i.data[2] ^ i.data[4] ^ i.data[5] ^ i.data[7]
        crcOut.next[22] = crcIn[2] ^ crcIn[3] ^ crcIn[5] ^ crcIn[6] ^ crcIn[30] ^ i.data[2] ^ i.data[3] ^ i.data[5] ^ i.data[6]
        crcOut.next[23] = crcIn[3] ^ crcIn[4] ^ crcIn[6] ^ crcIn[7] ^ crcIn[31] ^ i.data[3] ^ i.data[4] ^ i.data[6] ^ i.data[7]
        crcOut.next[24] = crcIn[0] ^ crcIn[2] ^ crcIn[4] ^ crcIn[5] ^ crcIn[7] ^ i.data[0] ^ i.data[2] ^ i.data[4] ^ i.data[5] ^ i.data[7]
        crcOut.next[25] = crcIn[0] ^ crcIn[1] ^ crcIn[2] ^ crcIn[3] ^ crcIn[5] ^ crcIn[6] ^ i.data[0] ^ i.data[1] ^ i.data[2] ^ i.data[3] ^ i.data[5] ^ i.data[6]
        crcOut.next[26] = crcIn[0] ^ crcIn[1] ^ crcIn[2] ^ crcIn[3] ^ crcIn[4] ^ crcIn[6] ^ crcIn[7] ^ i.data[0] ^ i.data[1] ^ i.data[2] ^ i.data[3] ^ i.data[4] ^ i.data[6] ^ i.data[7]
        crcOut.next[27] = crcIn[1] ^ crcIn[3] ^ crcIn[4] ^ crcIn[5] ^ crcIn[7] ^ i.data[1] ^ i.data[3] ^ i.data[4] ^ i.data[5] ^ i.data[7]
        crcOut.next[28] = crcIn[0] ^ crcIn[4] ^ crcIn[5] ^ crcIn[6] ^ i.data[0] ^ i.data[4] ^ i.data[5] ^ i.data[6]
        crcOut.next[29] = crcIn[0] ^ crcIn[1] ^ crcIn[5] ^ crcIn[6] ^ crcIn[7] ^ i.data[0] ^ i.data[1] ^ i.data[5] ^ i.data[6] ^ i.data[7]
        crcOut.next[30] = crcIn[0] ^ crcIn[1] ^ crcIn[6] ^ crcIn[7] ^ i.data[0] ^ i.data[1] ^ i.data[6] ^ i.data[7]
        crcOut.next[31] = crcIn[1] ^ crcIn[7] ^ i.data[1] ^ i.data[7]

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            ri.ready.next = ro.ready
            ro.valid.next = ri.valid
            ro.data.next = ri.data
            ro.last.next = ri.last
            if i.valid and ro.ready and i.last:
                fcs.next = ~crcOut
            if i.valid and ro.ready:
                if not first:
                    csum.next = crcOut
                else:
                    first.next = False
            if i.last:
                csum.next = 0xFFFFFFFF
                first.next = True
        
    return crc_logic, logic, axi4s_skidbuf_in_inst, axi4s_skidbuf_out_inst
