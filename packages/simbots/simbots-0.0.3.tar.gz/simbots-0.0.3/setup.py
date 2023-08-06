from setuptools import setup,find_packages

setup(
    name = "simbots",
    version = "0.0.3",
    description = "Simple bots or Simbots is a library designed to create simple bots using the power of python. This library utilises Intent,Entity,Relation and Context model to create bots . It uses a multinomial NB classifier to create intent classifiers.",
    packages =find_packages(),
    package_dir = {'':'src'},
    classifiers = ["Development Status :: 1 - Planning","Operating System :: OS Independent","License :: OSI Approved :: MIT License","Programming Language :: Python :: 3"],
    install_requires =['sklearn','objectpath'],
    license_files = ('LICENSE.txt')

)