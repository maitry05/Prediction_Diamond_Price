from pkg_resources import Requirement
from setuptools import find_packages,setup
from typing import List

# HYPHEN_E_DOT = "-e."

def get_requirements(file_path:str)->List[str]:
    requirement = []
    with open(file_path) as file_obj:
        requirement= file_obj.readlines()
        requirement= [req.replace("\n","") for req in requirement]

        # if HYPHEN_E_DOT in requirement:
            # requirement.remove(HYPHEN_E_DOT)
        return requirement
    

setup(
    name='DiamondPriceprediction',
    version='0.0.1',
    author='Maitry Patel',
    author_email='maitrypatel345@gmail.com',
    install_requires=get_requirements("requirement.txt"),
    packages=find_packages()
)