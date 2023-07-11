PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/templite/blob/main/{path}\#L{line}"
VERSION = $(shell $(PY) setup.py --version)

SOURCES = $(wildcard templite/*.py)

.PHONY: all clean distclean test push release

all: test README.md

clean:
	rm -f README.md *.json

distclean: clean
	rm -f -r tools
	rm -rf __pycache__ .mypy_cache

test:
	$(PY) -m unittest discover -v

push:
	git push origin HEAD

release:
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin HEAD
	git push origin tag v$(VERSION)

README.md: $(SOURCES) tools/py2doc.py tools/doc2md.py
	cat README.md.in > README.md
	echo '~~~' >> README.md
	$(PY) -m templite --help >> README.md
	echo '~~~' >> README.md
	echo "# Package documentation" >> README.md
	($(PY) tools/py2doc.py $(SOURCES) | \
	$(PY) tools/doc2md.py -l 2 -u $(URL) ) >> README.md

tools/py2doc.py: tools
	curl https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/py2doc.py -o $@

tools/doc2md.py: tools
	curl https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doc2md.py -o $@

tools:
	mkdir -p $@
