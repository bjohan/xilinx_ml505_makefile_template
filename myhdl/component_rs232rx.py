from myhdl import *
from interface_axi4s import Axi4sInterface
from component_axi4s_skidbuf import axi4s_skidbuf
from component_axi4s_connect import axi4s_connect
@block
def rs232rx(reset, clk, o, rxdi, baudDiv=100):
    baudTick = Signal(False)
    rxd = Signal(True)
    rxd0 = Signal(True)
    rxd1 = Signal(True)
    baudCnt = Signal(intbv(0, min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=11));
    rxData = Signal(intbv(0)[len(o.data):])
    ob = Axi4sInterface(len(o.data))
    i_skidbuf = axi4s_skidbuf(reset, clk, ob, o)
    #i_skidbuf = axi4s_connect(ob, o)

    @always_seq(clk.posedge, reset=reset)
    def logic():
        rxd1.next = rxdi
        rxd0.next = rxd1
        rxd.next = rxd0
        if currentBit > 0:
            baudCnt.next = baudCnt +1;
            if baudCnt == baudDiv:
                baudCnt.next = 0

                baudTick.next = True
            else:
                baudTick.next = False

        #Start bit detected, start the baud clock with half cycle delay
        if rxd == False and currentBit == 0:
            currentBit.next = 1;
            baudCnt.next = baudDiv >> 1;

        #Count the bits
        if baudTick and currentBit > 0:
            if currentBit < 10:
                currentBit.next = currentBit + 1
            else:
                currentBit.next = 0

        if currentBit > 1 and baudTick and currentBit < 10:
            rxData.next = rxData >> 1 
            rxData.next[len(rxData)-1]=rxd
            #ob.data.next[currentBit-2] = rxd
            currentBit.next = currentBit +1

        if currentBit == 10 and rxd == True and baudTick:
            ob.data.next = rxData
            ob.valid.next = True
        else:
            ob.valid.next = False
        if reset == True:
            baudTick.next = False
            baudCnt.next = 0
            currentBit.next = 0
    return logic, i_skidbuf
