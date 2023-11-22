PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/templite/blob/main/{path}\#L{line}"
VERSION = $(shell $(PY) setup.py --version)

SOURCES = $(wildcard templite/*.py)

.PHONY: all clean distclean test release

all: test README.md

clean:
	rm -f README.md *.json

distclean: clean
	rm -f templite/doctest_utils.py
	rm -r -f tools
	rm -r -f __pycache__ .mypy_cache

test: templite/doctest_utils.py
	$(PY) -m unittest discover -v

release:
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin HEAD
	git push origin tag v$(VERSION)

README.md: README.md.in $(SOURCES) tools/py2doc.py tools/doc2md.py
	cat README.md.in > README.md
	echo '# Usage' >> README.md
	echo '~~~' >> README.md
	$(PY) -m templite --help >> README.md
	echo '~~~' >> README.md
	echo "# Package documentation" >> README.md
	($(PY) tools/py2doc.py $(SOURCES) | \
	$(PY) tools/doc2md.py -l 2 -u $(URL) ) >> README.md

templite/doctest_utils.py:
	echo "# -*- coding: utf-8 -*-" > $@
	echo "" >> $@
	echo "################################################################################" >> $@
	echo "# DO NOT EDIT!!!" >> $@
	echo "# This file was downloaded from:" >> $@
	echo "# https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doctest_utils.py" >> $@
	echo "# and the Makefile will remove any change. " >> $@
	echo "###" >> $@
	echo "" >> $@
	curl https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doctest_utils.py >> $@

tools/py2doc.py: tools
	echo "# -*- coding: utf-8 -*-" > $@
	echo "" >> $@
	echo "################################################################################" >> $@
	echo "# DO NOT EDIT!!!" >> $@
	echo "# This file was downloaded from:" >> $@
	echo "# https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doctest_utils.py" >> $@
	echo "# and the Makefile will remove any change. " >> $@
	echo "###" >> $@
	echo "" >> $@
	curl https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/py2doc.py >> $@

tools/doc2md.py: tools
	echo "# -*- coding: utf-8 -*-" > $@
	echo "" >> $@
	echo "################################################################################" >> $@
	echo "# DO NOT EDIT!!!" >> $@
	echo "# This file was downloaded from:" >> $@
	echo "# https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doctest_utils.py" >> $@
	echo "# and the Makefile will remove any change. " >> $@
	echo "###" >> $@
	echo "" >> $@
	curl https://raw.githubusercontent.com/Kerrigan29a/microdoc/main/doc2md.py >> $@

tools:
	mkdir -p $@
