test:
	python -m unittest discover tests

run:
	python main.py

lint:
	python -m pylint pixel_sorting

type_check:
	python -m mypy pixel_sorting

.PHONY: test
