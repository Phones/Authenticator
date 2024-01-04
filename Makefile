run:
	python src/main.py

create_build:
	rm -rf build
	python setup.py build

build_installer_folder_linux:
	python build_linux_installer.py

# build_installer_linux:
# 	rm -rf Authenticator.deb
# 	rm -rf build
# 	make build
# 	rm -rf pacote_deb
# 	mkdir pacote_deb
# 	mkdir -p pacote_deb/DEBIAN
# 	mkdir -p pacote_deb/usr/bin
# 	mkdir -p pacote_deb/usr/share/applications
# 	mkdir -p pacote_deb/usr/share/icons
# 	cp build/exe.linux-x86_64-3.8/Authenticator pacote_deb/usr/bin
# 	cp build/exe.linux-x86_64-3.8/icons/cadeado64.ico pacote_deb/usr/share/icons
# 	cp authenticator.desktop pacote_deb/usr/share/applications
	
# 	sudo chown root:root -R pacote_deb/usr/bin/Authenticator
# 	sudo chmod 0755 pacote_deb/usr/bin/Authenticator
# 	echo "Package: Authenticator\nVersion: 1.0\nSection: utils\nPriority: optional\nArchitecture: amd64\nMaintainer: Paulo Henrique de Campos <paulohenriqueh178h@gmail.com>\nDescription: Programa de autenticação de 2 fatores MFA" > pacote_deb/DEBIAN/control

# 	sudo dpkg-deb --build pacote_deb Authenticator.deb

# teste:
# 	mv setup.py teste.py
# 	mv setup2.py setup.py
# 	python setup.py --command-packages=stdeb.command bdist_deb

# 	mv setup.py setup2.py
# 	mv teste.py setup.py
