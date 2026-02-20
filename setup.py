import os
import platform
from setuptools import Extension, setup
import sys


class PythonVersionError(Exception):
    pass


python_version = [int(i) for i in platform.python_version_tuple()]
py_ver = python_version[0]
py_subver = python_version[1]
if py_ver != 3:
    raise PythonVersionError(f"Python 3 required. Installed version is {py_ver}")
if py_subver not in range(8, 15):
    raise PythonVersionError("Setup requires Python >=3.8,<3.15")


NAME = "cythonpowered"
VERSION = "0.2.0"
LICENSE = "GNU GPLv3"
DESCRIPTION = "Cython-powered replacements for popular Python functions. And more."
AUTHOR = "Lucian Croitoru"
AUTHOR_EMAIL = "lucianalexandru.croitoru@gmail.com"
URL = "https://github.com/lucian-croitoru/cythonpowered"

KEYWORDS = ["python", "cython", "random", "performance"]
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: MacOS",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Get long_description from README
with open("README.md", "r") as f:
    long_description = f.read()

# Get CHANGELOG
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

long_description = long_description + "\n\n" + changelog


# Import Cython (guaranteed to be available via pyproject.toml build-requires)
from Cython.Build import cythonize

# Cython modules to build
CYTHON_MODULES = ["random", "dateutil"]

# Get Cython module information
cython_file_list = [
    {
        "module_name": f"{NAME}.{module}.{module}",
        "module_source": [
            os.path.join(NAME, module, "*.pyx"),
        ],
    }
    for module in CYTHON_MODULES
]


# Build Cython extensions
cython_module_list = []

for f in cython_file_list:
    extension = Extension(
        name=f["module_name"],
        sources=f["module_source"],
        language="c",
        # TODO: re-enable -fopenmp, handle arm64 arch
        # extra_compile_args=["-fopenmp"],
        # extra_link_args=["-fopenmp"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )
    cython_module_list.append(extension)


# Set build_ext --inplace argument explicitly
sys.argv = sys.argv + ["build_ext", "--inplace"]

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=[
        "cythonpowered",
        "cythonpowered.random",
        "cythonpowered.dateutil",
        "utils",
        "utils.benchmark",
        "utils.definitions",
    ],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    python_requires=">=3.8,<3.15",
    ext_modules=cythonize(module_list=cython_module_list, language_level="3"),
    package_data={"": ["*.pyx"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["cythonpowered=utils.main:main"],
    },
)
