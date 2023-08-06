#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="SymCircuit",
    version="0.1.0",
    author="Martok",
    author_email="martok@martoks-place.de",
    description="Symbolic electronic circuit analysis",
    long_description=open("README.md","rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/martok/py-symcircuit",
    project_urls={
        "Bug Tracker": "https://github.com/martok/py-symcircuit/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "sympy",
    ],
    extras_require={
        "EE": [
            "networkx",
            "numpy",
            "mplotkit"
        ],
    },
)
