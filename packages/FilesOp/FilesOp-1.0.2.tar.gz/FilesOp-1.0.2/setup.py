import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FilesOp", # Replace with your own username
    version="1.0.2",
    author="King Kaito Kid",
    author_email="djstrix@me.com",
    description="Gestionale dei file per usi interni",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KingKaitoKid/FileOperations",
    packages=setuptools.find_packages(),
    #install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.6',
)