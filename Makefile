SHELL := bash

.PHONY: all \
		clean clean-output clean-keys \
		config \
		key \
		sign \
		verify \
		benchmark

all: clean config key sign verify benchmark

clean: clean-output clean-keys

clean-output:
	rm -rf images/outputs

clean-keys:
	rm -rf keys/

config:
	py src/config.py

key:
	py src/keyGen.py

sign:
	py src/sigGen.py

verify:
	py src/sigVer.py

benchmark:
	py src/benchmark.py