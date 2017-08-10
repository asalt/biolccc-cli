from setuptools import setup

def calculate_version(inputfile):
    version_list =  [x.split('\'')[1] for x in open(inputfile, 'r')
                     if x.startswith('__version__')]
    if version_list:
        return version_list[0]
    else:
        return '1.0'

package_version = calculate_version('main.py')
setup(
    name='biolccc-cli',
    version=package_version,
    py_modules=['main'],
    install_requires=[
        'Click',
        'pyteomics.biolccc'
    ],
    entry_points="""
    [console_scripts]
    biolccc-cli=main:main
    """,
    python_requires="<=3.0",
)
