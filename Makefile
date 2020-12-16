egg:
	@python setup.py bdist_egg

PY_FILES=`find . -name '*.py' -not -path '*./build' -not -path './setup.py'`
style:
	@flake8 --show-source --max-line-length=80 $(PY_FILES)
