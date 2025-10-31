"""
cellSNP - Analysis of expressed alleles in single cells
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
exec(open("./cellSNP/app.py").read())

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding = 'utf-8') as f:
    long_description = f.read()
    
reqs = ['numpy', 'pysam>=0.15.2']

setup(
    name='cellSNP',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = __version__,

    description = 'cellSNP - Genotyping Bi-Allelic SNPs on Single Cells',
    long_description = long_description,
    url = 'https://github.com/single-cell-genetics/cellSNP',

    author = 'Xianjie Huang and Yuanhua Huang',
    author_email = 'xianjie5@connect.hku.hk and yuanhua@ebi.ac.uk',

    license = 'Apache-2.0',
    keywords = ['allelic expression', 'single-cell RNA-seq'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = find_packages(),

    entry_points={
          'console_scripts': [
              'cellSNP = cellSNP.cellSNP:main'
              ],
          }, 

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    
    install_requires = reqs,

    py_modules = ['cellSNP'],

    # Cython extensions
    #ext_modules = cythonize([Extension(**opts) for opts in ext_modules], language_level = sys_version.major),

    # Setting 'use_2to3 = True' to provide a facility to invoke 2to3 on the code as a part of the build process.
    # UPDATE-250919: new version of setuptools complains "error in cellSNP setup command: use_2to3 is invalid."
    #use_2to3 = True

    # buid the distribution: python setup.py sdist
    # upload to pypi: twine upload dist/...

)
