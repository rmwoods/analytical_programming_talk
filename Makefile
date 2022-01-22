SHELL := /bin/bash
PYTHON_INTERPRETER = python3.9

env:
	$(PYTHON_INTERPRETER) -m venv env
	source env/bin/activate && pip install -U pip pip-tools setuptools wheel

requirements.txt: requirements.in env
	source env/bin/activate && pip-compile -r -o requirements.txt requirements.in

environment: requirements.txt env
	source env/bin/activate && pip install -r requirements.txt

test:
	source env/bin/activate && pytest

data:
	mkdir data

get_data: data
	wget https://raw.githubusercontent.com/rmwoods/teaching/master/my_data.csv -O data/my_data.csv

data/my_data.csv: get_data

results_for_kari:# env data/my_data.csv
	source env/bin/activate && python calc_stuff.py -i data/my_data.csv -o data/high_accels.csv

results_for_clare:# env data/my_data.csv
	source env/bin/activate && python calc_stuff.py -i data/my_data.csv -o data/high_accels_smooth5.csv -s 5
