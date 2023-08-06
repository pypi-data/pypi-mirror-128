# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyconvertio",
    version="0.1.0",
    description="Convert your files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Henrique Pires",
    author_email="pireshenrique22@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    package_dir={"":".."},
    packages=["pyconvertio"],
    include_package_data=True,
    install_requires=["tqdm"]
)