import os

print("Deleta a pasta build antiga")
os.system("rm -rf build")

print("Deleta a pasta authenticator-installer-linux-v1.0 antiga")
os.system("rm -rf authenticator-installer-linux-v1.0")

print("Builda o executavel")
os.system("make create_build")

build_path = "build/"
folder_name = os.listdir(build_path)[0]

print("Renomeia a pasta com os arquivos de instalação")
folder_path = f"{build_path}/{folder_name}"
new_folder_path = f"{build_path}Authenticator"
os.system(f"mv {folder_path} {new_folder_path}")

print("Cria a pasta de logs do programa")
os.mkdir(f"{new_folder_path}/Logs")

print("Cria pasta para instalação no linux")
os.mkdir("authenticator-installer-linux-v1.0")

print("Copia os arquivos de instalação para a pasta de instalação")
os.system(f"cp -p -r {new_folder_path} authenticator-installer-linux-v1.0/")

print("Deleta a pasta build vazia")
os.system("rm -rf build")

print("Seta permissão para o arquivo install.sh")
os.system("sudo chmod +x install.sh")

print("Copia o arquivo de instalação")
os.system("cp -p install.sh authenticator-installer-linux-v1.0/")

print("Copia o arquivo Authenticator.desktop do programa")
os.system("cp -p Authenticator.desktop authenticator-installer-linux-v1.0/")

print("Zipa a pasta de instalação")
os.system("zip -r authenticator-installer-linux-v1.0.zip authenticator-installer-linux-v1.0")

print("Zip de instalação para linux finalizado!")
