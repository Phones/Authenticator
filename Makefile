build:
	python setup.py build

build_instaler_linux:
	dpkg-deb --build build/ Authenticator.deb