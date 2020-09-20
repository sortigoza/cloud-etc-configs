import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")


def fpath(name):
    return os.path.join(ROOT, name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read("README.md")


def get_version():
    init = open(os.path.join(ROOT, "cloud_etc_configs", "__init__.py")).read()
    return VERSION_RE.search(init).group(1)


requires = ["toolz", "pydantic"]

setup(
    name="cloud-etc-configs",
    version=get_version(),
    url="https://github.com/sortigoza/cloud-etc-configs",
    license="MIT",
    author="sortigoza",
    author_email="sortigoza.jobs@gmail.com",
    description="application configuration sync tool",
    long_description=desc(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"cloud_etc_configs": ["examples/*.md"]},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
