from myhdl import *

@block
def mdio_interface(reset, clk, i, o, t, mdc, rw, phyAddr, regAddr, dataWrite, dataRead, startTransfer, busy, baudDivHalf=5):

    t_State = enum('S_IDLE', 'S_TRANSFER');

    preamble = Signal(modbv(1)[32:])
    start = Signal(modbv(1)[2:])
    write = Signal(modbv(1)[2:])
    read = Signal(modbv(2)[2:])
    turnAround = Signal(modbv(1)[2:])
    state = Signal(t_State.S_IDLE)

    if len(phyAddr) != 5:
        raise TypeError("phyAddr must be 5 bits long")
    if len(regAddr) != 5:
        raise TypeError("regAddr must be 5 bits long")
    if len(dataWrite) != 16:
        raise TypeError("dataWrite must be 16 bits long")

    commandBits = len(preamble)+len(start)+len(write)+len(phyAddr)+len(regAddr)
    totalBits = commandBits+len(turnAround)+len(dataWrite)
    currentBit = Signal(intbv(0, min=0, max=totalBits+1));

    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    completeWord = Signal(modbv(0)[totalBits:])
    readFlag = Signal(False)
    mdcs = Signal(False)
    dataReads = Signal(modbv(0)[len(dataRead):])

    @always_comb
    def out_reg():
        dataRead.next = dataReads
        mdc.next = mdcs

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            if state == t_State.S_IDLE:
                if rw:
                    completeWord.next = concat(preamble, start, read, phyAddr, regAddr, turnAround, dataWrite)
                else:
                    completeWord.next = concat(preamble, start, write, phyAddr, regAddr, turnAround, dataWrite)

                if startTransfer:
                    readFlag.next=rw
                    state.next = t_State.S_TRANSFER
                    currentBit.next = 0
                    busy.next = 1
                    baudCnt.next = 0
                    t.next = 0
            elif state == t_State.S_TRANSFER:
                baudTick.next = False
                baudCnt.next = baudCnt +1;
                if baudCnt == baudDivHalf:
                    baudCnt.next = 0
                    if mdcs:
                        mdcs.next = False
                        baudTick.next = True
                    else:
                        mdcs.next = True
                   
                if baudTick: 
                    currentBit.next = currentBit+1
                    o.next = completeWord[totalBits-1]
                    completeWord.next = completeWord << 1
                    if currentBit+1 == totalBits:
                        busy.next = 0
                        state.next = t_State.S_IDLE
                        t.next = 0
                    if currentBit+1 == commandBits and readFlag:
                        t.next = 1
                    if currentBit > commandBits+1 and readFlag:
                        dataReads.next = dataReads << 1
                        dataReads.next[0] = i

    return logic, out_reg
