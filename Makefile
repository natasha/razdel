
test:
	pytest -vv \
		--pep8 --flakes razdel \
		--int 100 \
		--cov-report term-missing --cov-report xml --cov razdel

full:
	pytest --int 10000 razdel

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
