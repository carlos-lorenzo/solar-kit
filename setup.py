from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.1.1"
DESCRIPTION = "Visualise a solar system and do cool stuff with it"

# Setting up
setup(
    name="solarkit",
    version=VERSION,
    author="Carlos Lorenzo",
    author_email="<clorenzozuniga@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["numpy", "pandas", "matplotlib"],
    keywords=["solar system", "space", "astrophysics", "bpho"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)