from setuptools import setup, find_packages
from pkg_resources import parse_requirements

def get_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.read().splitlines()
    return [str(req) for req in parse_requirements(requirements)]

requirements = get_requirements('/home/paulo/Authenticator/requirements.txt')

setup(
    name='Authenticator',
    version='1.0',
    author='Paulo Henrique de Campos',
    url='https://github.com/Phones/Authenticator',
    author_email='paulohenriqueh178h@gmail.com',
    description='Programa para autenticação de dois fatores',
    packages=find_packages(),
    install_requires=requirements,
    long_description='Programa para autenticação de dois fatores'
)