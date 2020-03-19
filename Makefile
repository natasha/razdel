
test:
	pytest -vv --pep8 --flakes razdel

int:
	pytest -vv razdel --int

ci:
	pytest -vv --pep8 --flakes razdel --int --cov razdel --cov-report xml

wheel:
	python setup.py bdist_wheel

version:
	bumpversion minor

upload:
	twine upload dist/*

clean:
	find . \
		-name '*.pyc' \
		-o -name __pycache__ \
		-o -name .DS_Store \
		| xargs rm -rf
	rm -rf dist/ build/ .cache/ .ipynb_checkpoints/ .pytest_cache/ \
		.coverage *.egg-info/
