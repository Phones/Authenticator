#!/bin/bash

# ------ Cores ------
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
ORANGE='\033[38;5;216m'
NC='\033[0m'
# -------------------

# ------------------  print with color -----------------------
function pwc()
{
    text_color=${1^^}
    text=${2^^}

    echo -e "\e${!text_color} ${text} ${NC}"
}
# ------------------------------------------------------------

check_path_exist_and_deleted()
{
    local path="$1"
    if [ -e "$path" ]; then
        pwc "orange" "O caminho '$path' existe. Deletando para substituir pelo novo."
        sudo rm -rf $path
    else
        echo "O caminho '$path' não existe."
    fi 
}

program_path="/opt/"
folder_name="Authenticator"
pwc "blue" "Verifica se o caminho da pasta do pragama existe. Se sim, deleta, para receber a nova"
check_path_exist_and_deleted "$program_path$folder_name"

# Caminho para instalar o programa
pwc "blue" "Copia os arquivos do programa"
sudo cp -p -r $folder_name $program_path

pwc "blue" "Seta as permissões necessarias"
folder_program_path="$program_path$folder_name"
sudo chmod -R 755 $folder_program_path
sudo chown -R $USER:$USER $folder_program_path

pwc "blue" "Verifica se o caminho do arquivo desktop do pragama existe no /home/paulo/.local/share. Se sim, deleta, para receber o novo"
file_name=Authenticator.desktop
program_desktop_path2="/home/$USER/.local/share/applications/"
check_path_exist_and_deleted "$program_desktop_path2$file_name"

pwc "blue" "Copia o arquivo desktop do programa"
sudo cp -p $file_name $program_desktop_path2

pwc "blue" "Atualiza o cache de aplicativos"
update-desktop-database ~/.local/share/applications/

pwc "green" "Instalação finalizada com sucesso"
