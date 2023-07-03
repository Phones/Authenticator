#!/bin/bash

# Caminho para instalar o programa
program_path="/opt/"
echo "Copia os arquivos do programa"
sudo cp -r Authenticator $program_path

file_path_="/opt/Authenticator/authenticator"
echo "Seta a permissão necessaria"
sudo chmod +x $program_path

program_desktop_path="/usr/share/applications/"
# program_desktop="[Desktop Entry]\nName=Authenticator\nVersion=1.0\nComment=Programa para autenticação de dois fatores.\nExec=/opt/Authenticator/authenticator\nIcon=/opt/Authenticator/icons/cadeado64.png\nTerminal=false\nType=Application\nCategories=Aplicativos;\n"
# sudo echo $program_desktop > $program_desktop_path
sudo cp Authenticator.desktop $program_desktop_path

program_desktop_path2="/home/paulo/.local/share/applications/"
# sudo echo $program_desktop > $program_desktop_path2
sudo cp Authenticator.desktop $program_desktop_path2

echo "Atualiza o cache de aplicativos"
update-desktop-database ~/.local/share/applications/

echo "Instalação finalizada com sucesso"
