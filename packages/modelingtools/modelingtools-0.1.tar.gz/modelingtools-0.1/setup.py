import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modelingtools",
    version="0.1",
    author="Jeremy Miller",
    author_email="jeremymiller00@gmail.com",
    description="Tools to make modeling easier - Work in progress",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremymiller00/modelingtools",
    project_urls={
        "Bug Tracker": "https://github.com/jeremymiller00/modelingtools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.7",
)