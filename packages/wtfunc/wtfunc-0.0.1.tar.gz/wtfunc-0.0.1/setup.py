import sys

import setuptools

sys.path.insert(0, "src")
import wtfunc

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="wtfunc",
    version=wtfunc.__version__,
    author="Kevin Musgrave",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KevinMusgrave/wtfunc",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
    install_requires=[],
    extras_require={},
)
