from myhdl import *

from interface_axi4s import Axi4sInterface
from component_axi4s_appender import axi4s_appender

def convert_axi4s_appender(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    i = Axi4sInterface(8)
    o = Axi4sInterface(8)  
    prependData = Signal(intbv(0xD1D0)[16:])
    axi4s_appender_inst = axi4s_appender(reset, clk, i, o, prependData)

    axi4s_appender_inst.convert(hdl=hdl);


convert_axi4s_appender(hdl='VHDL')
