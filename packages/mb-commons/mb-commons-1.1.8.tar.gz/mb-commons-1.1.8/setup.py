import codecs
import os
import re

import setuptools


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="mb-commons",
    version=find_version("mb_commons/__init__.py"),
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "requests==2.26.0",
        "PySocks==1.7.1",
        "sorcery==0.2.2",
        "pydash==5.1.0",
        "wrapt==1.13.3",
        "python-dateutil==2.8.2",
        "pymongo==3.12.1",
        "pydantic==1.8.2",
        "python-dotenv==0.19.2",
    ],
    extras_require={
        "dev": [
            "pytest==6.2.5",
            "pre-commit==2.15.0",
            "pytest-xdist==2.4.0",
            "wheel==0.37.0",
            "twine==3.6.0",
        ],
    },
)
