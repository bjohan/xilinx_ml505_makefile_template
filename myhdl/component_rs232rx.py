from myhdl import *

@block
def rs232rx(reset, clk, o, rxd, baudDiv=100):
    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=11));
    rxData = Signal(intbv(0)[len(o.data):])

    @always(clk.posedge)
    def logic():
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
            #o.data.next[currentBit-2] = rxd
            currentBit.next = currentBit +1

        if currentBit == 10 and rxd == True and baudTick:
            o.data.next = rxData
            o.valid.next = True
        else:
            o.valid.next = False
        if reset == True:
            baudTick.next = False
            baudCnt.next = 0
            currentBit.next = 0
    return logic
