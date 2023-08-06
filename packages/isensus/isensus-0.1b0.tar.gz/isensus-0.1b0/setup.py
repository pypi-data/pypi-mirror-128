from pathlib import Path
from setuptools import setup, find_packages


def _get_version():
    # read isensus/version.py and return
    # the version
    path = Path() / "isensus" / "version.py"
    with open(path) as version_file:
        ns = {}
        exec(version_file.read(), ns)
    return ns["__version__"]


# no pip dependencies for now
_dependencies = []

setup(
    name="isensus",
    version=_get_version(),
    description="Utility for tracking status of MPI-IS IT users",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vincent Berenz",
    author_email="vberenz@tuebingen.mpg.de",
    url="https://github.com/MPI-IS/isensus.git",
    maintainer="Vincent Berenz - Max Planck Institute for Intelligent Systems",
    packages=find_packages(),
    license="bsd",
    python_requires=">=3.5",
    install_requires=_dependencies,
    scripts=["bin/isensus"],
)
