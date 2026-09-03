HHY ?= hhy

.PHONY: check test run-example

check:
	$(HHY) check lib/hhyweb.hhy examples/hello/app.hhy examples/api/app.hhy examples/dashboard/app.hhy tests/framework.hhy
	$(HHY) fmt --check lib/hhyweb.hhy examples/hello/app.hhy examples/api/app.hhy examples/dashboard/app.hhy tests/framework.hhy
	sh -n bin/hhy-web

test: check
	$(HHY) run tests/framework.hhy
	HHY=$(HHY) python3 tests/smoke.py

run-example:
	$(HHY) serve --dev examples/hello/app.hhy -- 8000
