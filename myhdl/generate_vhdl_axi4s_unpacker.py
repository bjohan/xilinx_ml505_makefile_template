from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_unpacker import axi4s_unpacker

def convert_axi4s_unpacker(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8);
    outRegs = Signal(intbv()[24:])
    valid = Signal(False)
    ready = Signal(False)
    axi4s_unpacker_inst = axi4s_unpacker(reset, clk, i, outRegs, 8, valid, ready )
    axi4s_unpacker_inst.convert(hdl=hdl);


convert_axi4s_unpacker(hdl='VHDL')
