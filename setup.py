#lets setup our project as local package  #if you pip list u wont find this project so thats why we have to locally setup 
# -e . in requirements.txt it will auto sets up

from setuptools import find_packages, setup

setup(
    name = 'Generative AI Project',
    version= '0.0.0',
    author= 'Anuriti Gupta ',
    author_email= 'anuritigupta26@gmail.com',
    packages= find_packages(),
    install_requires = []

)