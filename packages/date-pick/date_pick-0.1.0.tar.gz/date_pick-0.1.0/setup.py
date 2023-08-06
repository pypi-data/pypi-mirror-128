from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

with open("version") as file:
    version = file.read().strip()

setup(
    name="date_pick",
    packages=["date_pick"],
    version=version,
    license="MIT",
    description="Pick date by conditions and list of re-like wildcards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nick Kuzmenkov",
    author_email="nickuzmenkov@yahoo.com",
    url="https://bitbucket.org/Vnk260957/date_pick.git",
    keywords=["datetime", "regexp"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
