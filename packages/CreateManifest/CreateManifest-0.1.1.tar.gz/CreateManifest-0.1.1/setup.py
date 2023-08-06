from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CreateManifest',
    version='0.1.1',
    description='Package to create manifest file',
    Long_description=open('README.rst').read(),
    author='Nitesh Agarwal',
    author_email='nitesh.agarwal@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

