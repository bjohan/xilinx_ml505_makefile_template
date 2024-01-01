COMPONENTS = $(wildcard test_*.py)
VCDS = $(COMPONENTS:.py=.vcd)
NAMES_WITH_SUFFIX = $(patsubst test_%,% ,$(COMPONENTS))
VHDLS = $(patsubst %.py, %.vhd, $(NAMES_WITH_SUFFIX))
SIMULATION_SOURCES = $(wildcard simulation_*.py)
SIMULATIONS = $(SIMULATION_SOURCES:.py=.vcd)
PYTHON = python3.6

test_%.vcd: test_%.py component_%.py
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

%.vhd: generate_vhdl_%.py component_%.py
	$(PYTHON) $<

simulation_%.vcd: simulation_%.py
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

.PHONY: clean simuations vhdls tests all
tests: $(VCDS)

vhdls: $(VHDLS)

simulations: $(SIMULATIONS)

all: tests vhdls simulations

clean:
	rm -f $(VCDS) $(VHDLS) $(SIMULATIONS) pck_myhdl_011.vhd
	
