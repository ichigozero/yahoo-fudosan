from setuptools import find_packages, setup

setup(
    name='yahoo_fudosan',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
