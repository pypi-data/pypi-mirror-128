from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.8.0'
DESCRIPTION = 'Strings and numbers'
LONG_DESCRIPTION = 'A package that allows to identify vowels and consonants in stringand reverse numbers and find divisible'

# Setting up
setup(
    name="fun_with_py",
    version=VERSION,
    author="HSD",
    author_email="<ashuhemantsingh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'vowels', 'consonants', 'count'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)