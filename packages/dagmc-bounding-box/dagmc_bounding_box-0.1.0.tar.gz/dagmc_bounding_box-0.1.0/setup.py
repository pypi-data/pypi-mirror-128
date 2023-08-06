import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dagmc_bounding_box",
    version="0.1.0",
    author="The Fusion Energy Development Team",
    author_email="mail@jshimwell.com",
    description="Find the bounding box and other related properties of a DAGMC h5m file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/dagmc_bounding_box",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["meshio", "trimesh"],
)
