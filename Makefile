VERSION = $(shell python3 setup.py --version)

push:
	git push origin HEAD

release:
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin HEAD
	git push origin tag v$(VERSION)
