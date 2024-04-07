from myhdl import *

from interface_axi4s import Axi4sInterface
from component_dpbram_fifo import dpbram_fifo
from component_axi4s_skidbuf import axi4s_skidbuf

@block
def axi4s_ethernet_valid_framer(reset, clk, rxdata, rx_dv, o):
    rxdatar = Signal(intbv(0)[len(rxdata):])
    rxdatarr = Signal(intbv(0)[len(rxdata):0])
    rx_dvr = Signal(False)
    rx_dvrr = Signal(False)

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset: 
            rxdatar.next = rxdata
            rxdatarr.next = rxdatar

            rx_dvr.next = rx_dv 
            rx_dvrr.next = rx_dvr
            o.data.next = rxdatarr
            o.valid.next = rx_dvrr
            if rx_dvrr and not rx_dvr:
                o.last.next = True
            else:
                o.last.next = False
                
        
    return logic
