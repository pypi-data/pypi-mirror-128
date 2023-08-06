#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="mplotkit",
    version="0.0.7",
    author="Martok",
    author_email="martok@martoks-place.de",
    description="Collection of helpers for plotting with matplotlib",
    long_description=open("README.md","rt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/martok/py-plotkit",
    project_urls={
        "Bug Tracker": "https://github.com/martok/py-plotkit/issues",
    },
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
    install_requires=[
        "matplotlib"
    ],
    python_requires=">=3.6",
)
