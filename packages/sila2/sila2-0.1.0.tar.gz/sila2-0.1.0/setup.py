from distutils.dir_util import copy_tree
from glob import glob
from os import makedirs
from os.path import basename, dirname, join
from shutil import copy

from setuptools import find_packages, setup

base_dir = dirname(__file__)
package_dir = "src"
name = "sila2"

test_requirements = [
    "pytest",
    "pytest-cov",  # pytest: code coverage
]
code_quality_requirements = [
    "flake8",  # style checker
]


def copy_resources_from_sila_base():
    resource_dir = join(base_dir, package_dir, name, "resources")
    makedirs(resource_dir, exist_ok=True)

    # xsd
    copy_tree(join(base_dir, "sila_base", "schema"), join(resource_dir, "xsd"))

    # xsl
    makedirs(join(resource_dir, "xsl"), exist_ok=True)
    for file in glob(join(base_dir, "sila_base", "xslt", "*.xsl")):
        copy(file, join(resource_dir, "xsl", basename(file)))

    # proto
    makedirs(join(resource_dir, "proto"), exist_ok=True)
    copy(
        join(base_dir, "sila_base", "protobuf", "SiLAFramework.proto"),
        join(resource_dir, "proto", "SiLAFramework.proto"),
    )
    copy(
        join(base_dir, "sila_base", "protobuf", "SiLABinaryTransfer.proto"),
        join(resource_dir, "proto", "SiLABinaryTransfer.proto"),
    )


copy_resources_from_sila_base()

setup(
    name=name,
    version="0.1.0",
    author="Niklas Mertsch",
    author_email="niklas.mertsch@stud.uni-goettingen.de",
    description="Python implementation of the SiLA 2 standard for lab automation",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sila2/sila_python",
    project_urls={
        "Source": "https://gitlab.com/sila2/sila_python",
        "Bug Reports": "https://gitlab.com/sila2/sila_python/-/issues",
        "SiLA Standard": "https://sila-standard.org",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(where=package_dir),
    package_dir={"": package_dir},
    install_requires=[
        "black",
        "grpcio",
        "grpcio-tools",
        "isort",
        "jinja2",
        "lxml",
        "jsonschema",
        "xmlschema",
        "zeroconf",
    ],
    python_requires=">=3.7",
    extras_require=dict(
        tests=test_requirements,
        dev=test_requirements + code_quality_requirements,
    ),
    include_package_data=True,
)
