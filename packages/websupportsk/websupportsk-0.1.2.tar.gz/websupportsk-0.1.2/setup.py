from setuptools import setup
from setuptools import find_packages
from os import path

version = "0.1.2"

install_requires = [
    "requests"
]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf8") as f:
    long_description = f.read()

setup(
    name="websupportsk",
    version=version,
    description="Python wrapper for the Websupport.sk REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JozefGalbicka/python-websupportsk",
    author="Jozef Galbicka",
    author_email="alerts.cryp@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: Name Service (DNS)"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
