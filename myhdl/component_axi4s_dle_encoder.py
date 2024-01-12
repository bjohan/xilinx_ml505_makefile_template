from myhdl import *
from component_axi4s_appender import axi4s_appender
from component_axi4s_prepender import axi4s_prepender
from component_escaper import escaper
t_State = enum('S_TRANSFER', 'S_APPEND');

@block
def axi4s_dle_encoder(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn,
        tDataOut, tValidOut, tReadyIn, tLastOut):

    tDataEscaped = Signal(intbv(0)[8:])
    tValidEscaped = Signal(False)
    tReadyEscaped = Signal(False)
    tLastEscaped = Signal(False)

    tDataPre = Signal(intbv(0)[8:])
    tValidPre = Signal(False)
    tReadyPre = Signal(False)
    tLastPre = Signal(False)

    prependData = Signal(intbv(0x02C0)[16:])
    appendData = Signal(intbv(0x03C0)[16:])


    escape_inst = escaper(reset, clk, 
        tDataIn, tValidIn, tReadyOut, tLastIn, 
        tDataEscaped, tValidEscaped, tReadyEscaped, tLastEscaped,
        0xc0)

    prepend_inst = axi4s_prepender(reset, clk, 
        tDataEscaped, tValidEscaped, tReadyEscaped, tLastEscaped,
        tDataPre, tValidPre, tReadyPre, tLastPre,
        prependData)

    
    append_inst = axi4s_appender(reset, clk, 
        tDataPre, tValidPre, tReadyPre, tLastPre,
        tDataOut, tValidOut, tReadyIn, tLastOut,
        appendData)

        
    return escape_inst, prepend_inst, append_inst
