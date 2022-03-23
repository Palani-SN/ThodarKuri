from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ThodarKuri",
    version="1.0.0",
    description="Generic Recursive Template Engine for Parsing and Filling",
    py_modules=["ThodarKuri/Filler", "ThodarKuri/Parser"],
    package_dir={"": "SRCS"},
    packages=['ThodarKuri','ThodarKuri/Grammer'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Palani-SN/ThodarKuri",
    author="Palani-SN",
    author_email="psn396@gmail.com",

    install_requires = [
        "blessings ~= 1.7",
        "lark >= 1.0.0",
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
            "requests >= 2.26.0",
        ],
    },
)
