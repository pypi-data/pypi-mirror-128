import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orbit-pkg-SERGEI-DOLIN",
    version="0.0.0",
    author="Frazer McLean",
    author_email="frazer@frazermclean.co.uk",
    description="lib for edu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SergeyDolin/Orbit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "Orbital"},
    packages=setuptools.find_packages(where="Orbital"),
    python_requires=">=3.8",
)