from myhdl import *
from interface_axi4s import Axi4sInterface
from component_axi4s_unpacker import axi4s_unpacker
from component_axi4s_packer import axi4s_packer
from component_mdio_interface import mdio_interface
from functions.function_ids import functionId
t_State = enum('S_IDLE', 'S_BC_RESP', 'S_TRANSFER', 'S_PRE_TRANSFER', 'S_RESPOND' );

@block
def function_mdio_interface(reset, clk, i, o, mdio_in, mdio_out, mdio_tristate, mdio_clk):
    bw = len(i.data) #bus width 
    hww = 32 #Header word witdth
    myFunctionId = Signal(intbv(functionId['mdio_interface'])[hww:]) 


    state = Signal(t_State.S_IDLE)
    inWords = Signal(intbv(0)[hww:])
    inValid = Signal(False)
    inReady = Signal(False)
    currentWord = Signal(modbv(0)[hww:])

    outWords = Signal(modbv(0)[hww:])
    outValid = Signal(False)
    outReady = Signal(False)
    
    nWords = Signal(intbv(0, min = 0, max = int(len(outWords)/len(i.data))+1))
    tooLong = Signal(False)
    txOne = Signal(False)

    phyAddr = Signal(modbv(0)[5:])
    regAddr = Signal(modbv(0)[5:])
    regDataWrite = Signal(modbv(0)[16:])
    regDataRead = Signal(modbv(0)[16:])
    start = Signal(False)
    busy = Signal(False)
    read = Signal(False)
    
    i_unpacker = axi4s_unpacker(reset, clk, i, outWords, outValid, outReady, nWords, tooLong)
    i_mdio_interface = mdio_interface(reset, clk, mdio_in, mdio_out, mdio_tristate, mdio_clk, read, phyAddr, regAddr, regDataWrite, regDataRead, start, busy, 20)
    i_packer = axi4s_packer(reset, clk, o, inWords, inValid, inReady, txOne)

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_IDLE:
            txOne.next = 0
            outReady.next = 0
            inValid.next = 0
            if outValid:
                if outWords[bw:0] == modbv(-1)[bw:]:
                    #Send obligatory broadcast response that is a package only containning function id
                    state.next = t_State.S_BC_RESP
                    inWords.next[bw:0] = myFunctionId
                    inValid.next = 1
                    txOne.next = 1
                    outReady.next = 1
                else:
                    read.next = outWords[0]
                    phyAddr.next = outWords[6:1]
                    regAddr.next = outWords[11:6]
                    regDataWrite.next = outWords[32:16]
                    start.next = 1
                    outReady.next = 1
                    state.next = t_State.S_PRE_TRANSFER

        if state == t_State.S_BC_RESP:
            outReady.next = 0
            if inReady:
                inValid.next = 0
                state.next = t_State.S_IDLE

        if state == t_State.S_PRE_TRANSFER:
            start.next = 0
            outReady.next = 0
            state.next = t_State.S_TRANSFER
        if state == t_State.S_TRANSFER:
            if busy == 0 and inReady:
                inWords.next[0] = read
                inWords.next[6:1] = phyAddr
                inWords.next[11:6] = regAddr
                if read:
                    inWords.next[32:16] = regDataRead
                else:
                    inWords.next[32:16] = regDataWrite
                state.next = t_State.S_IDLE
                inValid.next = 1

    return logic, i_unpacker, i_packer, i_mdio_interface

