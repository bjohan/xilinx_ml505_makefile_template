COMPONENTS = $(wildcard test_*.py)
VCDS = $(COMPONENTS:.py=.vcd)
NAMES_WITH_SUFFIX = $(patsubst test_%,% ,$(COMPONENTS))
VHDLS = $(patsubst %.py, %.vhd, $(NAMES_WITH_SUFFIX))
PYTHON = python3.6

test_%.vcd: test_%.py component_%.py
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

%.vhd: generate_vhdl_%.py component_%.py
	$(PYTHON) $<

.PHONY: clean simuations vhdlstest
simulations: $(VCDS)

vhdls: $(VHDLS)

clean:
	rm -f $(VCDS) $(VHDLS) pck_myhdl_011.vhd
	
test:
	echo $(COMPONENTS)
	echo $(NAMES_WITH_SUFFIX)
	echo $(VHDLS)
