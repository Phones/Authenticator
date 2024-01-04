run:
	python src/main.py

create_build:
	rm -rf build
	python setup.py build

build_installer_folder_linux:
	python build_linux_installer.py
