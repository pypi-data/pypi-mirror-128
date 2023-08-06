import os
import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# This call to setup() does all the work
setup(
    name="backend_workshop_microservices_common",
    version="1.0",
    description="Qustodio backend_workshop_microservices common repo",
    url="https://github.com/qustodio/backend_workshop_microservices",
    license="MIT",
    author="Qustodio developers",
    author_email="info@qustodio.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
    packages=find_packages(include=['common', 'common.*']),
    include_package_data=False,
    install_requires=[
        "grpcio-tools==1.27.1"
    ],
    setup_requires=['flake8']
)
