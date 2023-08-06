import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FilesOp",
    version="1.0.0",
    author="KingKaitoKid",
    author_email="kingkaitokid10@gmail.com",
    description="Pacakge for internal use of project to read files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KingKaitoKid/FileOperations",
    project_urls={
        "Bug Tracker": "https://github.com/KingKaitoKid/FileOperations/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)