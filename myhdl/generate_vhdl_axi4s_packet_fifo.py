from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_packet_fifo import axi4s_packet_fifo

def convert_axi4s_packet_fifo(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    discard = Signal(False)
    
    i = Axi4sInterface(8); 
    o = Axi4sInterface(8);
    
    frameLength = Signal(modbv(0)[16:]) 

    axi4s_packet_fifo_inst = axi4s_packet_fifo(reset, clk, i, discard, o, frameLength, 1024)
    axi4s_packet_fifo_inst.convert(hdl=hdl);


convert_axi4s_packet_fifo(hdl='VHDL')
