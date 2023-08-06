from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="AbiHandler",
    version="0.0.1",
    author="tinghsuwan",
    author_email="wanth1997@gmail.com",
    description="Handler for abi",
    license="MIT",
    url="https://github.com/LeagueOfBlockchain/AbiHandler",
    packages=["abi_handler"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["web3", "loguru", ""],
    zip_safe=True,
)
