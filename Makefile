
test:
	pytest -vv --pep8 --flakes razdel

int:
	pytest -vv razdel --int

ci:
	pytest -vv --pep8 --flakes razdel --int --cov razdel --cov-report xml

clean:
	find razdel -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
