from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'Information Equivalence for Cubic regression Model'
LONG_DESCRIPTION = 'A STUDY OF EXACT DESIGNS IN CUBIC REGRESSION MODEL  IN PERSPECTIVE OF DE LA GARZA PHENOMENON '

# Setting up
setup(
    name="Infequevalence",
    version=VERSION,
    author="Developer Rohit",
    author_email="143rohitbehera@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['Infequevalence'],
    install_requires=['numpy'],
    keywords=['python', 'Information Equevalence', 'DE LA GARZA PHENOMENON', 'EXACT DESIGNS', 'developerrohit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
