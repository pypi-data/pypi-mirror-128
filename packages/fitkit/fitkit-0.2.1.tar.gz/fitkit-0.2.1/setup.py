import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fitkit",
    version="0.2.1",
    author="Gabriel Okasa and Kenneth Younge",
    author_email="gabriel.okasa@epfl.ch",
    description="Fit and inspect statistical models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okasag/fitkit.git",
    packages=["fitkit/", ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)