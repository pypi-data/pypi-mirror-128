from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Simplyfing the process of creation of cybersecurity tools'
LONG_DESCRIPTION = 'A package that allows to build hacking tools without any efforts. Hence it simplifies the process of security testing in an enviornment where there are no readymade tools available'

# Setting up
setup(
    name="simplyhack",
    version=VERSION,
    author="Abhishek Uday Dangat",
    author_email="abshdangat@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['scapy', 'scapy_http', 'colorama'],
    keywords=['python', 'hacking', 'cybersecurity', 'hacking tools', 'security testing', 'hacker'],
)
