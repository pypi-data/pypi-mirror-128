from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='ar_one_qdk_beta',
    version='0.0.2',
    packages=find_packages(),
    author='Plyoushkin',
    author_email='plyoushkin.evgen@gmail.com',
    #long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'qodex_dk'
    ],
)
