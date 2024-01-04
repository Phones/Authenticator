import os
import platform
from cx_Freeze import setup, Executable
from pkg_resources import parse_requirements

# Função para obter as dependências do arquivo requirements.txt
def get_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.read().splitlines()
    return [str(req) for req in parse_requirements(requirements)]

def check_files_exit():
    keys_exist = os.path.exists("keys/.keys.txt")
    settings_ini_exist = os.path.exists("settings.ini")

    return keys_exist, settings_ini_exist

def create_empty_files():
    path_keys_file = "keys/.keys.txt"
    operational_system = platform.system()

    if not "Linux" in operational_system:
        path_keys_file = "keys\\.keys.txt"

    keys_exist, settings_ini_exist = check_files_exit()
    if not keys_exist:
        with open(path_keys_file, "w") as arquivo:
            pass

    if not settings_ini_exist:
        with open("settings.ini", "w") as arquivo:
            dark_theme = """[General]\ntheme=dark\n"""
            arquivo.write(dark_theme)

def get_base_and_icon_path():
    operational_system = platform.system()
    if  operational_system in "Linux":
        return None, "icons/cadeado64.ico"
    
    return "Win32GUI", "icons\cadeado64.ico"

# Cria os arquivos caso eles não existam
create_empty_files()

build_options = {
    "packages": [],
    "excludes": [],
    "include_files": [
        "keys/",
        "icons/",
        "settings.ini"
    ]
}

# Especifique a versão do Python que deseja usar
python_version = "3.8"
# Obtenha as dependências do arquivo requirements.txt
requirements = get_requirements('requirements.txt')

base, icon_path = get_base_and_icon_path()
# Defina os executáveis e opções
executables = [Executable("src/main.py", base=base, target_name="authenticator", icon=icon_path)]

# Crie o setup com as dependências
setup(
    name="NomeDoProjeto",
    version="1.0",
    description="Descrição do Projeto",
    options={"build_exe": build_options},
    executables=executables,
    install_requires=requirements,
    python_version=python_version
)