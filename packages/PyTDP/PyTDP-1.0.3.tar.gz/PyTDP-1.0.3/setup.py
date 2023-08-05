# -*- coding: utf-8 -*-
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

install_requires = [
  'googletrans==4.0.0-rc1',
  'pandas==1.1.5',
  'scikit-learn==0.22.2',
  'joblib==1.0.1'
]

packages = [
    'pytdp',
    'pytdp/bases',
    'pytdp/reader',
    'pytdp/preprocessor',
    'pytdp/TD',
    'pytdp/analyzer'
]

setup(
    name='PyTDP',
    version='1.0.3',
    license="MIT License",
    description="Makes troublesome data preprocessing comfortable",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TorDataScientist',
    url='https://github.com/TorDataScientist/PyTDP',
    packages=packages,
    install_requires=install_requires,
    #entry_points={'console_scripts': console_scripts},
    # other arguments omitted
)

