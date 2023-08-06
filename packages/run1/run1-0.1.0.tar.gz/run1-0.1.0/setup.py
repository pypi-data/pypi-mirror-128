from setuptools import setup, find_packages


setup(
    name='run1',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['cycler<0.10', 'matplotlib',],

)