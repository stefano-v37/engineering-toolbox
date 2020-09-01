import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EngineeringToolbox",
    version="0.0.1",
    author="Stefano Vanin",
    description="Learn by doing repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefano-v37/engineering-toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)