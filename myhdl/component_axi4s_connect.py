from myhdl import *

@block
def axi4s_connect(i, o):

    @always_comb
    def connect():
        o.valid.next = i.valid
        i.ready.next = o.ready
        o.data.next = i.data
        o.last.next = i.last

    return connect


@block
def axi4s_connect_no_last(i, o):

    @always_comb
    def connect():
        o.valid.next = i.valid
        i.ready.next = o.ready
        o.data.next = i.data

    return connect

