import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

# Default
version = "SNAPSHOT"

if "--version" in sys.argv:
    idx = sys.argv.index("--version")
    sys.argv.pop(idx)
    version = sys.argv.pop(idx)

print("Using version " + version)

setuptools.setup(
    name='py-canary-2',
    version=version,
    author="Brian Marks",
    description="Python API for the Canary App",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bm1549/canary",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
 )
