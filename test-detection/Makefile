.SHELL := /bin/sh
.DEFAULT_GOAL := zip
.PHONY = clean

test:
	rm setup.cfg; tox

run:
	cd .target; python3 test-detection.py