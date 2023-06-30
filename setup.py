import sys
from cx_Freeze import setup, Executable
from pkg_resources import parse_requirements

# Função para obter as dependências do arquivo requirements.txt
def get_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.read().splitlines()
    return [str(req) for req in parse_requirements(requirements)]

# Defina os executáveis e opções
executables = [
    Executable("main.py", base=None)
]

build_options = {
    "packages": [],
    "excludes": [],
    "include_files": [
        "Keys/",
        "icons/",
        "settings.ini"
    ]
}

# Especifique a versão do Python que deseja usar
python_version = "3.8"
# Obtenha as dependências do arquivo requirements.txt
requirements = get_requirements('requirements.txt')

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