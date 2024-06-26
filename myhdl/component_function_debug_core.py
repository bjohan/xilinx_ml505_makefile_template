from myhdl import *
from interface_axi4s import Axi4sInterface
from component_axi4s_unpacker import axi4s_unpacker
from component_axi4s_packer import axi4s_packer
from component_configurable_trigger import configurable_trigger
from component_dpbram_fifo import dpbram_fifo
from functions.function_ids import functionId
import math
t_State = enum('S_IDLE', 'S_BC_RESP1', 'S_BC_RESP2', 'S_WAIT_READY', 'S_TRANSMIT_FIFO', 'S_SET_OR_MASK' );
t_FifoState = enum('S_IDLE', 'S_FILLING', 'S_FULL');

@block
def function_debug_core(reset, clk, i, o, debug, depth):
    bw = len(i.data) #bus width 
    #myFunctionId = Signal(intbv(functionId['debug_core'])[len(i.data):]) 
    hww = 32 #Header word witdth
    myFunctionId = Signal(intbv(functionId['debug_core'])[hww:]) 
    nHeaderWords = 3
    nHeaderBits = nHeaderWords*hww
    headerStart = 0
    headerEnd = nHeaderBits
    debugStart = headerEnd
    debugEnd = debugStart+len(debug)


    state = Signal(t_State.S_IDLE)
    maxWords = nHeaderWords*int(hww/len(i.data))+math.ceil(len(debug)/len(i.data))
    referenceWord = Signal(modbv(-1)[len(debug):])
    careMask = Signal(modbv(-1)[len(debug):])
    inWords = Signal(intbv(0)[maxWords*bw:])
    inValid = Signal(False)
    inReady = Signal(False)
    currentWord = Signal(modbv(0)[hww:])

    outWords = Signal(modbv(0)[maxWords*bw:])
    outValid = Signal(False)
    outReady = Signal(False)
    
    nWords = Signal(intbv(0, min = 0, max = int(len(outWords)/len(i.data))+1))
    tooLong = Signal(False)
    txOne = Signal(False)

    triggerTrigged = Signal(False)
    armAnd = Signal(False)
    trigged = Signal(False)

    fifoState = Signal(t_FifoState.S_IDLE)
    fifoWrite = Signal(False)
    fifoReady = Signal(False)
    fifoDataOut = Signal(modbv(0)[len(debug):])
    fifoDataRead = Signal(False)
    fifoDataValid = Signal(False)
    fifoDataEmpty = Signal(False)
    fifoDataNew = Signal(False)
      
    
    i_unpacker = axi4s_unpacker(reset, clk, i, outWords, outValid, outReady, nWords, tooLong)
    i_packer = axi4s_packer(reset, clk, o, inWords, inValid, inReady, txOne)
    i_trigger = configurable_trigger(reset, clk, debug, referenceWord, careMask, triggerTrigged)
    i_dpbram_fifo=dpbram_fifo(reset, clk, debug, fifoWrite, fifoReady, fifoDataOut, fifoDataRead, fifoDataValid, fifoDataEmpty, fifoDataNew, depth)

    @always_comb
    def out_reg():
       trigged.next = (triggerTrigged and armAnd)
       fifoWrite.next = ((fifoState == t_FifoState.S_IDLE) and trigged) or (fifoState == t_FifoState.S_FILLING)
 
    @always_seq(clk.posedge, reset=reset)
    def logic():

        if fifoState == t_FifoState.S_IDLE:
            if trigged:
                fifoState.next = t_FifoState.S_FILLING
        if fifoState == t_FifoState.S_FILLING:
            if not fifoReady:
                fifoState.next = t_FifoState.S_FULL

        if state == t_State.S_IDLE:
            txOne.next = 0
            outReady.next = 0
            inValid.next = 0
            if outValid:
                if nWords == 1 and outWords[bw:0] == modbv(-1)[bw:]:
                    #Send obligatory broadcast response that is a package only containning function id
                    state.next = t_State.S_BC_RESP1
                    inWords.next[bw:0] = myFunctionId
                    inValid.next = 1
                    txOne.next = 1
                    outReady.next = 1
                elif outWords[hww:0] == 0x00000001 and nWords == maxWords:
                    referenceWord.next = outWords[debugEnd:debugStart]
                    outReady.next = 1
                elif outWords[hww:0] == 0x00000002 and nWords == maxWords:
                    careMask.next = outWords[debugEnd:debugStart]
                    outReady.next = 1
                elif outWords[hww:0] == 0x00000003 and nWords == maxWords:
                    armAnd.next = outWords[hww]
                    outReady.next = 1
                else:
                    outReady.next = 1
            if fifoState == t_FifoState.S_FULL:
                #fifoDataRead.next = 1
                state.next = t_State.S_TRANSMIT_FIFO
                currentWord.next = 0
                armAnd.next = 0
                fifoState.next = t_FifoState.S_IDLE

        if state == t_State.S_BC_RESP1:
            outReady.next = 0
            if inReady:
                #Send extra response containing lengths
                txOne.next = 0
                inWords.next[hww:0] = myFunctionId
                inWords.next[2*hww:hww] = len(debug)
                inWords.next[3*hww:2*hww] = depth
                inValid.next = 1
                state.next = t_State.S_BC_RESP2

        if state == t_State.S_BC_RESP2:
            if inReady:
                inValid.next = 0
                state.next = t_State.S_WAIT_READY

        if state == t_State.S_WAIT_READY:
            if inReady:
                state.next = t_State.S_IDLE

        if state == t_State.S_TRANSMIT_FIFO:
            if fifoDataEmpty:
                state.next = t_State.S_IDLE
                fifoDataRead.next = 0
            elif inReady and not fifoDataRead:
                inWords.next[hww:0] = len(debug)
                inWords.next[2*hww:hww] = depth-1
                inWords.next[3*hww:2*hww] = currentWord
                inWords.next[debugEnd:debugStart]=fifoDataOut
                inValid.next = 1
                fifoDataRead.next = 1
                currentWord.next = currentWord+1
            else:
                inValid.next = 0 
                fifoDataRead.next = 0
        
    return logic, i_unpacker, i_packer, i_trigger, i_dpbram_fifo, out_reg

