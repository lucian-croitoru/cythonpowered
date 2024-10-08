import os
import platform
from setuptools import Extension, setup
import subprocess
import sys
from cythonpowered import VERSION, MODULES as CYTHON_MODULES


class PythonVersionError(Exception):
    pass


python_version = [int(i) for i in platform.python_version_tuple()]
py_ver = python_version[0]
py_subver = python_version[1]
if py_ver != 3:
    raise PythonVersionError(f"Python 3 required. Installed version is {py_ver}")
if py_subver not in range(8, 12):
    raise PythonVersionError("Setup requires Python>=3.8,<3.12")


NAME = "cythonpowered"
LICENSE = "GNU GPLv3"
DESCRIPTION = "Cython-powered replacements for popular Python functions. And more."
AUTHOR = "Lucian Croitoru"
AUTHOR_EMAIL = "lucianalexandru.croitoru@gmail.com"
URL = "https://github.com/lucian-croitoru/cythonpowered"

KEYWORDS = ["python", "cython", "random", "performance"]
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
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
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
SETUP_REQUIRES = [
    "setuptools==74.1.3",
    "wheel==0.43.0",
    "Cython>=3.0.0",
    "packaging==24.0",
    "more-itertools==10.0.0",
    "jaraco.functools>=4.0.0",
    "jaraco.text>=4.0.0",
]
INSTALL_REQUIRES = ["psutil>=6.0.0", "py-cpuinfo>=9.0.0", "prettytable>=3.0.0"]
PYTHON_MODULES = [NAME, "utils", "utils.definitions", "utils.benchmark"]

install_cython = subprocess.Popen(["pip", "install"] + SETUP_REQUIRES)
install_cython.wait()

from Cython.Build import cythonize

# Get long_description from README
with open("README.md", "r") as f:
    long_description = f.read()

# Get CHANGELOG
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

long_description = long_description + "\n\n" + changelog


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
    packages=PYTHON_MODULES + [f"{NAME}.{module}" for module in CYTHON_MODULES],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    setup_requires=SETUP_REQUIRES,
    install_requires=SETUP_REQUIRES + INSTALL_REQUIRES,
    scripts=[],
    ext_modules=cythonize(module_list=cython_module_list, language_level="3"),
    package_data={"": ["*.pyx"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["cythonpowered=utils.main:main"],
    },
)
