from setuptools import find_packages, setup

setup(
    name='yahoo_fudosan',
    description=(
        'Yahoo! JAPAN real estate scraper modules'
    ),
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        '': ['logging.ini'],
    },
    install_requires=[
        'beautifulsoup4',
        'click',
        'selenium',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        yahoo_fudosan=yahoo_fudosan.__main__:main
    ''',
)
