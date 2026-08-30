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
if py_subver not in range(9, 15):
    raise PythonVersionError("Setup requires Python >=3.9,<3.15")


NAME = "cythonpowered"
VERSION = "0.4.0"
LICENSE = "MIT"
DESCRIPTION = "Cython-powered replacements for popular Python functions — compiled for performance."
AUTHOR = "Lucian Croitoru"
URL = "https://github.com/lucian-croitoru/cythonpowered"

KEYWORDS = ["python", "cython", "performance", "lightweight", "compiled"]
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: MacOS",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
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
CYTHON_MODULES = ["random", "dateutil", "textparse"]

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
        extra_compile_args=["-O2"],
        # -fopenmp (compile + link) is intentionally disabled for portability
        # (arm64/MSVC). Re-enable only if a module actually uses prange/parallel.
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
    url=URL,
    packages=[
        "cythonpowered",
        "cythonpowered.random",
        "cythonpowered.dateutil",
        "cythonpowered.textparse",
        "utils",
        "utils.benchmark",
        "utils.definitions",
    ],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    python_requires=">=3.9,<3.15",
    ext_modules=cythonize(
        module_list=cython_module_list,
        language_level="3",
        # Keep the safe Cython 3.x defaults explicit (AGENTS.md §7): never set
        # unsafe values at the build level; opt out only via per-module pragmas.
        compiler_directives={
            "boundscheck": True,
            "wraparound": True,
            "cdivision": False,
            "overflowcheck": False,
        },
    ),
    package_data={"": ["*.pyx"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["cythonpowered=utils.main:main"],
    },
)
