from myhdl import *
from component_axi4s_address_switch import axi4s_address_switch
from component_axi4s_address_merge import axi4s_address_merge
from component_axi4s_prepender import axi4s_prepender
from interface_axi4s import Axi4sInterface

t_State = enum('S_POLL_THROUGH', 'S_POLL_MERGE', 'S_TRANSFER_THROUGH', 'S_TRANSFER_MERGE');
t_MuxState = enum('S_POLL', 'S_THROUGH', 'S_MERGE') 


@block
def axi4s_address_branch(reset, clk, i_prev, o_prev, i_func, o_func, funcaddr, i_next, o_next):
    addrDelim = Signal(modbv(-1)[len(i_prev.data):])
    o_func_prepend = Axi4sInterface(len(i_prev.data))
    addr_switch_inst = axi4s_address_switch(reset, clk, i_prev, i_func, funcaddr, o_next)
    prepender_inst = axi4s_prepender(reset, clk, o_func, o_func_prepend, addrDelim)
    addr_merge_inst = axi4s_address_merge(reset, clk, i_next, o_func_prepend, funcaddr, o_prev)
    
    return addr_switch_inst, prepender_inst, addr_merge_inst
