build-ndeps:
	rm -rf dist/*
	pipenv run build
	pipenv run pip install dist/*.whl --no-deps --force-reinstall