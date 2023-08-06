import os
from setuptools import find_packages, setup

from src.__version__ import __version__


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()


setup(
    name="Euphoria-CLI",
    version=__version__,
    author="Vinay Dawani",
    author_email="vdawani6@gmail.com",
    description="A small CLI tool to fetch Euphoria's price and stats",
    license="GNU GPL v3",
    url="https://github.com/vinaydawani/euphoria-cli",
    keywords="euphoria WAGMI sWAGMI blockchain rebase token bonding staking bond stake",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "art", "requests", "web3", "halo"],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["euphoria = src.app:euphoria"]},
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "Natural Language :: English",
    ],
)
