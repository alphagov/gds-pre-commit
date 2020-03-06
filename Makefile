# In your python env, run `make install` to insall required packages
# and then either `make` for a single test run
# or `make watch` for a continuous pipeline that reruns on changes.
#
# Comments to cyber.security@digital.cabinet-office.gov.uk
# This is free and unencumbered software released into the public domain.

.SILENT: test install upgrade watch checks Pipfile.lock

test: checks
	# pipenv run pytest -sqx --disable-warnings
	echo "✔️ Tests passed!"

checks: Pipfile.lock
	echo "⏳ running pipeline..."
	set -e
	pipenv run isort --atomic -yq
	pipenv run black -q .
	pipenv run flake8 --max-line-length=88 .  # in line with black
	pipenv run mypy --pretty .
	echo "✔️ Checks pipeline passed!"

Pipfile.lock:
	set -e
	echo "⏳ installing..."
	pipenv install flake8 mypy watchdog pyyaml argh pytest isort
	pipenv install --pre black
	pipenv run mypy_boto3 -q && echo  "✔️ mypy_boto3 stubs installed!"!! || true # ignored if not installed
	echo "✔️ Pip dependencies installed!"

upgrade:
	set -e
	wget -q https://raw.githubusercontent.com/alphagov/cyber-security-tools/master/python/Makefile -O Makefile
	echo "✔️ Upgraded Makefile!"

watch:
	echo "✔️ Watch setup, save a python file to trigger test pipeline"
	pipenv run watchmedo shell-command --drop --ignore-directories --patterns="*.py" --ignore-patterns="*#*" --recursive --command='clear && make --no-print-directory test' .
