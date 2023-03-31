RUN := poetry run

format:
	$(RUN) isort ./autopampa
	$(RUN) black ./autopampa

test:
	$(RUN) pytest

