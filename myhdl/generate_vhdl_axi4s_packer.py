from myhdl import *
from interface_axi4s import Axi4sInterface

from component_axi4s_packer import axi4s_packer

def convert_axi4s_packer(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    o = Axi4sInterface(8);
    inRegs = Signal(intbv()[24:])
    valid = Signal(False)
    ready = Signal(False)
    txOne = Signal(False)
    axi4s_packer_inst = axi4s_packer(reset, clk, o, inRegs, valid, ready, txOne)
    axi4s_packer_inst.convert(hdl=hdl);


convert_axi4s_packer(hdl='VHDL')
