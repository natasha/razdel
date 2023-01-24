
test:
	flake8 razdel
	pytest -vv --int 100 razdel
