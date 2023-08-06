import os
from setuptools import setup, find_packages

with open(
    os.path.join(os.path.dirname(__file__), "requirements/common.txt"), "r"
) as fh:
    requirements = fh.readlines()

# import os
# thelibFolder = os.path.dirname(os.path.realpath(__file__))
# requirementPath = thelibFolder + '/requirements.txt'
# install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
# if os.path.isfile(requirementPath):
#     with open(requirementPath) as f:
#         install_requires = f.read().splitlines()
# setup(name="yourpackage", install_requires=install_requires, [...])

NAME = "binance-futures-python-sdk"
DESCRIPTION = (
    "This is a lightweight library that works as a connector to Binance Futures public API."
)
AUTHOR = "Futures"
URL = "https://git.toolsfdg.net/andrea-c/binance-futures-python-sdk"
VERSION = 1.7

about = {}

with open("README.md", "r") as fh:
    about["long_description"] = fh.read()

root = os.path.abspath(os.path.dirname(__file__))

if not VERSION:
    with open(os.path.join(root, "binance", "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    license="MIT",
    description=DESCRIPTION,
    long_description=about["long_description"],
    long_description_content_type="text/markdown",
    AUTHOR=AUTHOR,
    url=URL,
    keywords=["Binance", "Public API"],
    install_requires=[req for req in requirements],
    # install_requires=open('requirements/common.txt').readlines(),
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
