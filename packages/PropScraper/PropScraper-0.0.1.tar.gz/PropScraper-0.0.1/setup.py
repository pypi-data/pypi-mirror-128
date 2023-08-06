import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.rst")) as f:
        README = f.read()
except IOError:
    README = ""

requires = [
    "requests",
    "beautifulsoup4",
]

setup(
    name="PropScraper",
    version="0.0.1",
    author="Jordi Fernández",
    author_email="jordi.feca@gmail.com",
    description="Web scraper for real state websites",
    long_description=README,
    url="https://bitbucket.org/jfdez/propscraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
