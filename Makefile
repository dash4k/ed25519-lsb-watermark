SHELL := bash

.PHONY: all \
		clean clean-outputs clean-keys clean-benchmarks \
		config \
		key \
		sign \
		verify \
		benchmark \
		confusion-matrix \
		server

all: clean config key sign verify benchmark confusion-matrix

clean: clean-outputs clean-keys

clean-outputs:
	rm -rf images/outputs images/labeled

clean-keys:
	rm -rf keys/

clean-benchmarks:
	rm -rf benchmarks/

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

confusion-matrix:
	py src/confusionMatrix.py

server:
	py -m uvicorn server:app --port 8000