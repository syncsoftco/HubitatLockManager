import os
from setuptools import setup, find_packages

# Read the version from the version.py file
def read_version():
    version = {}
    with open(os.path.join("hubitat_lock_manager", "version.py")) as fp:
        exec(fp.read(), version)
    return version["__version__"]


# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hubitat_lock_manager",
    version=read_version(),
    packages=find_packages(),
    install_requires=["requests", "selenium"],
    entry_points={
        "console_scripts": [
            "hubitat-lock-manager=hubitat_lock_manager.main:main",
        ],
    },
    author="pseudonymous",
    author_email="syncboard@googlegroups.com",
    description="A library to manage smart locks within the Hubitat ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hubitat_lock_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
