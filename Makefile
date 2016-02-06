build: clean
	python setup.py sdist bdist_wheel

test:
	pep8 setup.py urwid_timed_progress examples

clean:
	$(RM) -fr build dist *.egg-info

very-clean: clean
	find . -name '*.pyc' | xargs rm -f

install:
	pip install --upgrade urwid pytest pep8 sphinx sphinx-autobuild
	pip install --upgrade --editable .

test-release: build test
	twine upload -r pypitest dist/*

release: build test
	twine upload dist/*


.PHONY: build test clean very-clean install test-release release
