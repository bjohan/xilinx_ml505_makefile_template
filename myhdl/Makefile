COMPONENTS = $(wildcard test_*.py)
VCDS = $(COMPONENTS:.py=.vcd)
NAMES_WITH_SUFFIX = $(patsubst test_%,% ,$(COMPONENTS))
VHDLS = $(patsubst %.py, %.vhd, $(NAMES_WITH_SUFFIX))
SIMULATION_SOURCES = $(wildcard simulation_*.py)
SIMULATIONS = $(SIMULATION_SOURCES:.py=.vcd)
PYTHON = pyenv/bin/python3

pyenv: 
	mkdir -p pyenv

$(PYTHON): pyenv
	python3 -m venv pyenv
	pyenv/bin/pip install git+https://github.com/myhdl/myhdl.git@master

test_%.vcd: test_%.py component_%.py $(PYTHON)
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

%.vhd: generate_vhdl_%.py component_%.py $(PYTHON)
	$(PYTHON) $<

simulation_%.vcd: simulation_%.py $(PYTHON)
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

.PHONY: clean simuations vhdls tests all
tests: $(VCDS)

vhdls: $(VHDLS)

simulations: $(SIMULATIONS)

all: tests vhdls simulations

clean:
	rm -f $(VCDS) $(VHDLS) $(SIMULATIONS) pck_myhdl_011.vhd
	rm -rf pyenv
	
