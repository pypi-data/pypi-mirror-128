from setuptools import setup
from setuptools import find_packages

"""Packaging tool for the Yeti python bindings and CLI utility."""

from setuptools import setup
from setuptools import find_packages

"""Returns contents of README.md."""
with open("README.md", "r", encoding="utf-8") as readme_fp:
    long_description = readme_fp.read()

setup(
    name="python3-pdns",
    version="1.0",
    description="Binding python for passiveDNS Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="passiveDNS threat intel api",
    url="https://github.com/PassivePDNS/pypdns",
    author="Sebastien Larinier @sebdraven",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    include_package_data=True,
    python_requires=">=3.8",
    zip_safe=False,
)
