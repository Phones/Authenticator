run:
	python src/main.py

create_build:
	rm -rf build
	rm -rf keys/.keys.txt
	touch keys/.keys.txt
	python src/setup.py build

build_installer_folder_linux:
	python build_linux_installer.py
