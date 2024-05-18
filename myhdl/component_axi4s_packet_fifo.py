from myhdl import *

from interface_axi4s import Axi4sInterface
from component_dpbram import dpbram
from component_dpbram_fifo import dpbram_fifo
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_READ', 'S_WAIT', 'S_TRANSFER_DIRECT', 'S_TRANSFER_WAIT');

#Fifo input data is committed on i.last. if discard is high during write, all 
#uncommitted data will be deleted. if discard is high at the same time as 
#i.last, data will be discarded.
@block
def axi4s_packet_fifo(reset, clk, i, discard, o, length_out, depth):
    #Constants
    bits=len(i.data)
    
    #Shadow registers for reading outputs
    i_readys = Signal(False)
    o_valids = Signal(False)
    o_lasts = Signal(False)

    #Write address registers
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    comittedAddress = Signal(modbv(0, min=0, max=depth))

    #Read address registers
    ra = Signal(modbv(0, min = 0 , max = depth))
   

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
    empty = Signal(True)
    full = Signal(False)
    nextFull = Signal(False)

    #pipeline registers representing delays in dpbram
    war = Signal(modbv(0, min = 0 , max = depth)) #Write available, address of data that is actually written and stored in dpbram
    rar = Signal(modbv(0, min = 0 , max = depth)) #read available, address of data that is actually presented on the output of dbpram
    lrar = Signal(modbv(-1, min = 0 , max = depth)) #Last addres, newly read address, no longer "valid"
    

    #Flags to indicate if dpbram data is valid. v and vr are a shift register to correspond to delay in dpbram
    v = Signal(False )
    vr = Signal(False)


    #signals for length fifo
    length_in = Signal(modbv(0, min=0, max=depth))
    length_inp1 = Signal(modbv(0, min=0, max=depth))
    length_in_ready = Signal(False)
    length_we = Signal(False)
    length_re = Signal(False)
    length_out_valid = Signal(False)
    length_empty = Signal(False)
    length_new_data = Signal(False)
    
    #instances
    dpbram_inst = dpbram(clk, w, waddr, writeWord, dout_a_notused, clk, wr_b_notused, ra, din_b_notused, readWord, depth)
    length_fifo_inst = dpbram_fifo(reset, clk, length_in, length_we, length_in_ready, length_out, length_re, length_out_valid, length_empty, length_new_data, 128)

    @always_comb
    def combinatorial_logic():
        #Pack data together with last
        writeWord.next[bits:0] = i.data
        writeWord.next[bits] = i.last
        o.data.next=readWord[bits:0]
        o_lasts.next = readWord[bits]

        length_inp1.next = length_in+1

        if waddr == lrar:
            full.next = True
        else:
            full.next = False
            
        if waddrp1 == lrar:
            nextFull.next = True
        else:
            nextFull.next = False
            

        #Logic to determine if write is performed
        if i.valid and i_readys:
            w.next = True
        else:
            w.next = False

        if r and o_lasts: #Trigger new read of length fifo when last is read
            length_re.next = True
        else:
            length_re.next = False


        #Logic to determine if read is performed
        if o.ready and o_valids:
            r.next = True
        else:
            r.next = False
    
        if war == ra:
            empty.next = True
        else:
            empty.next = False
    
        o_valids.next = v

        #Shadow register assignment
        i.ready.next = i_readys
        o.valid.next = o_valids
        o.last.next = o_lasts

    @always_seq(clk.posedge, reset=reset)
    def logic():
        #TODO implement non committance if fifo gets full during write
        if not reset:
            length_we.next = False
            #pipeline registers
            war.next = comittedAddress
            rar.next = ra

            #Write logic
            if nextFull or full: #Ready to accept more data
                i_readys.next=False
            else:
                i_readys.next=True

            if w: #data was actually written
                waddr.next = waddr+1
                waddrp1.next = waddrp1+1
                length_in.next = waddr+1-comittedAddress
                if i.last and discard == False:
                    comittedAddress.next = waddr+1
                    length_we.next = True

            if discard:
                waddr.next = comittedAddress
                waddrp1.next = comittedAddress+1

            #Read logic
            vr.next = v; #dpb
            if o.ready and not empty: #initialize read from dpbram
                ra.next = ra+1;
                v.next = True
            
            if o.ready:
                if r:
                    lrar.next = rar
                    if o_lasts: #Reset pipeline to cause delay enough to lengh fifo to be valid when next frame starts
                        ra.next = lrar+2
                        rar.next = lrar+2
                        v.next = 0
                        vr.next = 0
                    
            else: #Reset read pipeline if ready is not valid
                ra.next = lrar+1
                rar.next = lrar+1
                v.next = 0
                vr.next = 0



    return logic, dpbram_inst, length_fifo_inst, combinatorial_logic

