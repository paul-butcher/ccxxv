from setuptools import setup

setup(
    name='ccxxv',
    version='0.1.2',
    description='Crossword solving assistant',
    author='Paul Butcher',
    license='LGPL-3',
    packages=['ccxxv'],
    entry_points={
        'console_scripts': ['ccxxv = ccxxv:cli_main']
    },
    package_data={'ccxxv': ['wordlists/*']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Puzzle Games',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Programming Language :: Python :: 2.7'
    ]
)