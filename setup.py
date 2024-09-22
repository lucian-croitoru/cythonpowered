import os
from setuptools import Extension, setup
import subprocess
import sys
from cythonpowered import VERSION, MODULES as CYTHON_MODULES


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
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
]
SETUP_REQUIRES = ["Cython>=3.0.0", "setuptools>=74.0.0"]
INSTALL_REQUIRES = ["psutil>=6.0.0", "py-cpuinfo>=9.0.0"]
PYTHON_MODULES = [NAME, "scripts", "scripts.benchmark"]

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
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"],
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
        "console_scripts": ["cythonpowered=scripts.main:main"],
    },
)
