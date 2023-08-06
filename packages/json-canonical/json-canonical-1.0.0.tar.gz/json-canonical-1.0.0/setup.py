import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
def read_file(path):
    print(here)
    with open(path, 'r') as f:
        return f.read()


setup(
    name='json-canonical',
    version='1.0.0',
    author='Anas Kanhouch',
    author_email='anas.m.kan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AnasMK/json-canonical',
    license='Apache License',
    description='Conanicalize JSON in JCS format',
    long_description=read_file('%s/README.rst'% here),   
)

