from myhdl import *

from interface_axi4s import Axi4sInterface
from component_dpbram import dpbram
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_READ', 'S_WAIT', 'S_TRANSFER_DIRECT', 'S_TRANSFER_WAIT');

#Fifo input data is committed on i.last. if discard is high during write, all 
#uncommitted data will be deleted. if discard is high at the same time as 
#i.last, data will be discarded.
@block
def axi4s_packet_fifo(reset, clk, i, discard, o, depth):
    #Constants
    bits=len(i.data)
    
    #Shadow registers for reading outputs
    i_readys = Signal(False)
    o_valids = Signal(False)

    #Write address registers
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    comittedAddress = Signal(modbv(0, min=0, max=depth))

    #Read address registers
    raddr = Signal(modbv(0, min = 0 , max = depth))
    raddrp1 = Signal(modbv(1, min = 0 , max = depth))

    #Registers to connect to memory, data+last
    writeWord =  Signal(intbv(0)[bits+1:])
    readWord =  Signal(intbv(0)[bits+1:])

    #Registers for unused memory ports
    dout_a_notused = Signal(intbv(0)[bits+1:])
    wr_b_notused = Signal(False)
    din_b_notused = Signal(intbv(0)[bits+1:])

    #Signals for combinatorial logic
    w = Signal(False) #Will be high when a write is peformed
    r = Signal(False) #Will be high when a read is performed

    #pipeline registers representing delays in dpbram
    war = Signal(modbv(0, min = 0 , max = depth)) #Write available, address of data that is actually written and stored in dpbram
    rar = Signal(modbv(0, min = 0 , max = depth)) #read available, address of data that is actually presented on the output of dbpram
    lrar = Signal(modbv(-1, min = 0 , max = depth)) #Last addres, newly read address, no longer "valid"
    
    #instances
    dpbram_inst = dpbram(clk, w, waddr, writeWord, dout_a_notused, clk, wr_b_notused, raddr, din_b_notused, readWord, depth)

    @always_comb
    def combinatorial_logic():
        #Pack data together with last
        writeWord.next[bits:0] = i.data
        writeWord.next[bits] = i.last
        o.data.next=readWord[bits:0]
        o.last.next=readWord[bits]


        #Logic to determine if write is performed
        if i.valid and i_readys:
            w.next = True
        else:
            w.next = False

        #Logic to determine if read is performed
        if o.ready and o_valids:
            r.next = True
        else:
            r.next = False         

        #Logic to determine if read data is valid
        if rar == war:
            o_valids.next = False
        else:
            if lrar != rar:
                o_valids.next = True
            else:
                o_valids.next = False

        #Shadow register assignment
        i.ready.next = i_readys
        o.valid.next = o_valids


    @always_seq(clk.posedge, reset=reset)
    def logic():
        #TODO implement non committance if fifo gets full during write
        if not reset:

            #pipeline registers
            war.next = comittedAddress
            rar.next = raddr

            #Write logic
            if waddrp1 == raddr:
                i_readys.next=False
            else:
                i_readys.next=True

            if w:
                waddr.next = waddr+1
                waddrp1.next = waddrp1+1
                if i.last:
                    comittedAddress.next = waddr+1

            if discard:
                waddr.next = comittedAddress
                waddrp1.next = comittedAddress+1

            #Read logic
            if r:
                raddr.next = raddr+1
                lrar.next = rar
                    


    return logic, dpbram_inst, combinatorial_logic

