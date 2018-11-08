
test:
	pytest -vv --pep8 --flakes razdel

clean:
	find razdel -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
