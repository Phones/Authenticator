import os

print("Deleta a pasta build antiga")
os.system("rm -rf build")

print("Deleta a pasta AuthenticatorSetup antiga")
os.system("rm -rf AuthenticatorSetup")

print("Builda o executavel")
os.system("make build")

build_path = "build/"
folder_name = os.listdir(build_path)[0]

print("Renomeia a pasta com os arquivos de instalação")
folder_path = f"{build_path}/{folder_name}"
new_folder_path = f"{build_path}/Authenticator"
os.system(f"mv {folder_path} {new_folder_path}")

print("Cria pasta para instalação no linux")
os.system("mkdir AuthenticatorSetup")

print("Copia os arquivos de instalação para a pasta de instalação")
os.system(f"mv {new_folder_path} AuthenticatorSetup/")

print("Seta permissão para o arquivo install.sh")
os.system("sudo chmod +x install.sh")

print("Copia o arquivo de instalação")
os.system("cp install.sh AuthenticatorSetup/")

print("Copia o arquivo .desktop do programa")
os.system("cp Authenticator.desktop AuthenticatorSetup/")

print("Zipa a pasta de instalação")
os.system("zip -r authenticator-linux-installer-v1.0.zip AuthenticatorSetup")

print("Deleta a pasta build antiga")
os.system("rm -rf build")

print("Zip de instalação para linux finalizado!")
