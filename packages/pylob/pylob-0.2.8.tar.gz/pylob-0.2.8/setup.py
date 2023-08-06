import pathlib
from glob import glob
from setuptools import setup

from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext


__version__ = "0.2.8"

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


ext_modules = [
    Pybind11Extension(
        "trades",
        sources=sorted(glob("pylob/trades/*.cpp")),
        language="c++",
        cxx_std=11,
        include_dir=[
            "pybind11/include"
        ]
    )
]

# This call to setup() does all the work
setup(
    name="pylob",
    version=__version__,
    description="Limit Order Book python module",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/deltaleap/pylob",
    author="Mattia Terenzi",
    author_email="gammalightened@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["pylob"],
    include_package_data=True,
    install_requires=[
        "sortedcontainers==2.4.0",
    ],
    cmd_class={"build_ext": build_ext},
    ext_modules=ext_modules,
    zip_safe=False,
)
