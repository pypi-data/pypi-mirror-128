"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils

from setuptools import setup, find_packages

setup(
    name = "Self-Check-Algorithm-Model",
    version = "1.0.5",
    description = "Self-Check-Algorithm-Model",
    long_description = "Self-Check-Algorithm-Model",
    license = "MIT Licence",
    url = "https://gitlab.com/ancientchaos/Self-Check-Algorithm-Model.git",
    author = "ancientchaos",
    author_email = "ancientchaos@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
)
