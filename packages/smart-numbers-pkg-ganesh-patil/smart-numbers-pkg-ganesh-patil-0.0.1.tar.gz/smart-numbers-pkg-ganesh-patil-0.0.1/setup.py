import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smart-numbers-pkg-ganesh-patil",
    # Replace with your own username above
    version="0.0.1",
    author="Ganesh Patil",
    author_email="ganeshpatil.1997@gmail.com",
    description="This is a test library created by Ganesh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)