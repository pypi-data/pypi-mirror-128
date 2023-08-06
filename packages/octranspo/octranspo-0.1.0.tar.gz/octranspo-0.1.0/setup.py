# pylint: disable=missing-module-docstring
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="octranspo",
    version="0.1.0",
    author="Adam Thompson-Sharpe",
    author_email="adamthompsonsharpe@gmail.com",
    description="A Python wrapper around the OC Transpo API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=("LICENSE-APACHE", "LICENSE-MIT"),
    url="https://gitlab.com/MysteryBlokHed/greasetools",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests~=2.25",
    ],
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires="~=3.8",
)
