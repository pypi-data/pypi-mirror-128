
from setuptools import setup, find_packages
from os import path
import glob
import SRPSTATS
import os

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Look for script files
lscr = glob.glob(os.path.join('Scripts', 'SRP*'))
lscrex = []
for i in lscr:
    if os.path.splitext(i)[1] == '':
        lscrex.append(i)


setup(
    name='SRPAstro.STATS', 
    version=SRPSTATS.__version__, 
    description='Statistical tools under SRP', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pypi.python.org/pypi/SRPAstro.STATS',
    author='Stefano Covino',
    author_email='stefano.covino@inaf.it',
    classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Unix',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 3',
                   ],
    keywords='astronomy data analysis',
    packages=find_packages(),
    python_requires='>=3',
    scripts=lscrex,
    install_requires=['SRPAstro','emcee>=3','ptemcee','scipy','numpy','pandas'],
    ) 

