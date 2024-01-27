from myhdl import *
from component_axi4s_appender import axi4s_appender
from component_axi4s_prepender import axi4s_prepender
from component_escaper import escaper
t_State = enum('S_TRANSFER', 'S_APPEND');

from interface_axi4s import Axi4sInterface

@block
def axi4s_dle_encoder(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn,
        tDataOut, tValidOut, tReadyIn, tLastOut):

    escaped = Axi4sInterface(8);    
    pre = Axi4sInterface(8);    
    
    prependData = Signal(intbv(0x02C0)[16:])
    appendData = Signal(intbv(0x03C0)[16:])


    escape_inst = escaper(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn, 
        escaped.data, escaped.valid, escaped.ready, escaped.last,
        0xc0)

    prepend_inst = axi4s_prepender(reset, clk,  escaped, pre, prependData)

    
    append_inst = axi4s_appender(reset, clk, 
        pre.data, pre.valid, pre.ready, pre.last,
        tDataOut, tValidOut, tReadyIn, tLastOut,
        appendData)

        
    return escape_inst, prepend_inst, append_inst
