SHELL := bash

.PHONY: all \
		clean clean-output clean-keys \
		config \
		key \
		sign \
		verify

all: clean config key sign verify

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