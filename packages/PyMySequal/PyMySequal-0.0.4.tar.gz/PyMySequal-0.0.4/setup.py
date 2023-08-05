from setuptools import setup, find_packages
import codecs
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="PyMySequal",
    version='0.0.4',
    author="Murali Tharan S",
    author_email="muralififa@gmail.com",
    description='A Smiple MsSql API',
    long_description_content_type="text/markdown",
    #long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyodbc',
        'pandas'],
    keywords=['SQL','MsSql','SQL using python','Pyodbc','SQL Connection'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)