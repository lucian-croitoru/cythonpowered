from Cython.Build import cythonize
import os
from setuptools import Extension, setup
import sys


NAME = "cythonpowered"
VERSION = "0.0.1"
LICENSE = "GNU GPLv3"
DESCRIPTION = "Cython-powered replacements for popular Python functions. And more."
AUTHOR = "Lucian Croitoru"
AUTHOR_EMAIL = "lucianalexandru.croitoru@gmail.com"
URL = "https://github.com/lucian-croitoru/cythonpowered"

MODULES = ["random"]
KEYWORDS = ["python", "cython", "random", "performance"]
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
]

# Get long_description from README
with open("README.md", "r") as f:
    long_description = f.read()


# Get Cython module information
cython_file_list = []
cython_module_list = []

for module in MODULES:
    module_dir = os.path.join(os.getcwd(), NAME, module)
    cython_file_list += [
        {
            "module_name": f"{NAME}.{module}.{module}",
            "module_source": os.path.join(module_dir, f),
        }
        for f in os.listdir(module_dir)
        if f.endswith(".pyx")
    ]


# Build Cython extensions
for f in cython_file_list:
    module_name = f["module_name"]
    module_source = f["module_source"]

    extension = Extension(
        name=module_name,
        sources=[module_source],
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
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=[NAME],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    install_requires=["Cython>=3.0.0"],
    scripts=[],
    ext_modules=cythonize(module_list=cython_module_list, language_level="3"),
)
